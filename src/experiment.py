# Class for holding the experiment results
import datetime
import pandas as pd
from exp_config import roi_column_prefix

class Experiment:
    def __init__(self, description, date, session_id):
        self.description = description
        if date is None:
            self.date = datetime.datetime.now()
        else:
            self.date = date
        self.session_id = session_id
        # Dataframe for holding the results
        self.results = None
        self.training_data = None
        self.number_of_rois = None
    
    def set_results(self, results: pd.DataFrame):
        self.results = results
    
    def set_training_data(self, training_data: pd.DataFrame):
        self.training_data = training_data
    
    def set_number_of_rois(self, number_of_rois: int):
        self.number_of_rois = number_of_rois

    # Returns the roi activity for a given roi number where trial number is a given trial number
    def get_roi_activity_by_trial(self, roi_number: int, trial_number: int):
        return self.results[self.results['trial_number'] == trial_number][f'{roi_column_prefix}{roi_number}'].values
    
    # Returns the number of trials in the experiment
    def get_number_of_trials(self):
        return len(self.results['trial_number'].unique())
    
    # Returns the number of rois in the experiment
    def get_number_of_rois(self):
        return self.number_of_rois
    
    # Get activity for all rois for a given trial number
    def get_trial_activity(self, trial_number: int):
        return self.results[self.results['trial_number'] == trial_number][[f'{roi_column_prefix}{i+1}' for i in range(self.number_of_rois)]].values

