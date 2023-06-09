from datetime import timedelta
from enum import Enum
from functools import reduce
import pandas as pd
import numpy as np
from experiment import Experiment
from exp_config import ConfigParams
from utils import get_locations_of_differences

# An enum representing the different types of experiments results files
class ExperimentResultsType(Enum):
    roi_results = 1
    external_data_results = 2
    training_data_results = 3

# a function that gets an experiment results type and returns the delimiter for the file
def get_delimiter(results_type: ExperimentResultsType):
    if results_type == ExperimentResultsType.roi_results:
        return ','
    elif results_type == ExperimentResultsType.external_data_results:
        return '\t'
    elif results_type == ExperimentResultsType.training_data_results:
        return ','

# A class for reading the experiment results, merging into one dataframe, and creating a new experiment object
class ExperimentBuilder:
    def __init__(self, experiment_description: str, session_id: int, roi_sampling_rate: int):
        self.experiment_description = experiment_description
        self.session_id = session_id
        # The sampling rate of the results dataframe in hertz
        self.roi_sampling_rate = roi_sampling_rate
        # List of files to read for the experiment
        self.files_to_read = []
        # Trial times list. Deprecated for now until the trial times in the user data file will be fixed.
        self.trial_times = None
        # Trial start indices list. Infered from the external data file until the trial times will be fixed.
        self.trial_start_indices = None
        # Results dataframe
        self.results = None
        # Training data dataframe
        self.training_data = None
        # Number of rois
        self.number_of_rois = None
        
    # Add a file to read for the experiment
    def add_file_to_read(self, file_path: str, results_type: ExperimentResultsType):
        self.files_to_read.append((file_path, results_type))
    
    # Read the files and merge into one dataframe
    def read_files(self):
        for file_path, results_type in self.files_to_read:
            if results_type == ExperimentResultsType.roi_results:
                self.read_roi_results(file_path)
            elif results_type == ExperimentResultsType.external_data_results:
                self.read_external_data_results(file_path)
            elif results_type == ExperimentResultsType.training_data_results:
                self.read_training_data_results(file_path)

    # Read the training data file, filter only the relevant session, and set the trial times list
    def read_training_data_results(self, file_path: str):
        df = pd.read_csv(file_path, delimiter=get_delimiter(ExperimentResultsType.training_data_results))
        df = df[df['session_id'] == self.session_id].reset_index(drop=True)
        # Set the trial times list, doesn't work for now because the trial times in the user data file are wrong.
        self.set_trial_times(df)
        self.training_data = df
    
    # Read the roi results file and extents the results dataframe
    def read_roi_results(self, file_path: str):
        df = pd.read_csv(file_path, delimiter=get_delimiter(ExperimentResultsType.roi_results))
        df = df.iloc[:, 1:]
        self.number_of_rois = df.shape[1]
        if self.results is None:
            self.results = df
        else:
            self.results = pd.concat([self.results, df], axis=1)

    # Read the external data, which is larger than the roi results, reduces the external data to 
    # the roi results size acording to the size of the current results dataframe
    def read_external_data_results(self, file_path: str):
        assert self.results is not None, 'ROI results must be read before external data results'
        self.external_data = pd.read_csv(file_path, delimiter=get_delimiter(ExperimentResultsType.external_data_results))
        # TODO: we assume that both dataframes represent the same time interval
        sampling_positions = np.linspace(0, self.external_data.shape[0], self.results.shape[0], endpoint=False, dtype=int)
        self.external_data = self.external_data.iloc[sampling_positions, :]
        # extend the results dataframe with the external data
        self.results = pd.concat([self.results.reset_index(drop=True), self.external_data.reset_index(drop=True)], axis=1)
        
    
    # Gets a column dataframe of the trial times and sets the trial times list.
    # Converts the trial times from a string to a datetime object
    # Normailizes the trial times to the first trial time
    # Deprecated. See the comment in the trial_times variable.
    def set_trial_times(self, df: pd.DataFrame):
        self.trial_times = df['mouseEntryTime'].tolist()
        self.trial_times = [pd.to_datetime(time) for time in self.trial_times]
        self.trial_times = [time - self.trial_times[0] for time in self.trial_times]
        # Remove the first trial time, which is 0
        self.trial_times = self.trial_times[1:]
        # Add a large time after the last trial to make sure the last trial is included
        self.trial_times += [timedelta(seconds=10000000000000)]
    
    # Sets the trial start indices list according to the training data file.
    def set_trial_start_indices(self):
        assert self.training_data is not None, 'Training data must be read before setting trial start indices'
        self.trial_start_indices = [0] + get_locations_of_differences(self.results['E-phys'], threshold=1, greater_than=False)

    # Add a new column to the results dataframe with the trial number according to the trial times list
    # The results sampling rate is the roi sampling rate
    # Deprecated. See the comment in the trial_times variable.
    def add_trial_number_column_by_trial_times(self):
        assert self.results is not None, 'ROI results must be read before adding trial number column'
        assert self.trial_times is not None, 'Trial times must be read before adding trial number column'
        trial_number = []
        current_sample_time = 0
        current_trial = 0
        for i in range(self.results.shape[0]):
            trial_number.append(current_trial)
            current_sample_time += 1 / self.roi_sampling_rate
            if timedelta(seconds=current_sample_time) >= self.trial_times[trial_number[-1]]:
                current_trial += 1
        self.results['trial_number'] = trial_number

    # Add a new column to the results dataframe with the trial number according to the trial indices list
    def add_trial_number_column_by_trial_indices(self):
        assert self.results is not None, 'ROI results must be read before adding trial number column'
        assert self.trial_start_indices is not None, 'Trial start indices must be read before adding trial number column'
        trial_number = [[i]*(self.trial_start_indices[i]  - self.trial_start_indices[i-1]) for i in range(1,len(self.trial_start_indices))]
        trial_number = reduce(lambda x,y: x+y, trial_number)
        trial_number += [trial_number[-1]]*(self.results.shape[0] - len(trial_number))
        self.results['trial_number'] = trial_number

    # Read all the files and create an experiment object
    def get_experiment(self):
        self.read_files()
        self.set_trial_start_indices()
        self.add_trial_number_column_by_trial_indices()
        exp = Experiment(self.experiment_description, None, self.session_id)
        exp.set_results(self.results)
        exp.set_training_data(self.training_data)
        exp.set_external_data(self.external_data)   
        exp.set_number_of_rois(self.number_of_rois)
        return exp
    

# Build an experiment object from a given config object
def build_experiment_from_config(config: ConfigParams):
    builder = ExperimentBuilder(config.experiment_description, config.session_id, config.roi_sampling_rate)
    builder.add_file_to_read(config.get_roi_path(), ExperimentResultsType.roi_results)
    builder.add_file_to_read(config.get_external_data_path(), ExperimentResultsType.external_data_results)
    builder.add_file_to_read(config.get_training_data_path(), ExperimentResultsType.training_data_results)
    return builder.get_experiment()

if __name__ == "__main__":
    from exp_config import ConfigParams
    config = ConfigParams()
    exp = build_experiment_from_config(config)
    # print every 100 row of the results dataframe with no truncation
    pd.set_option('display.max_rows', None)
    print(exp.results.iloc[::100, :])
    print(exp.external_data.iloc[::100, :])
