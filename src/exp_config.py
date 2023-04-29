import os

# TODO: Get the params from a config file or from the user
class ConfigParams:
    def __init__(self):
        # exp data folder
        self.exp_data_folder = 'exp_data'
        # Path to roi file
        self.roi_path = '02_stable_Results.csv'
        self.roi_sampling_rate = 40
        # path to external data file
        self.external_data_path = 'data_user_input.txt'
        # TODO: Verify external data sampling rate
        self.external_data_sampling_rate = 12000
        # path to training data file
        self.training_data_path = 'TrainingBox4_2022-11-02-modified.csv'
        # session id
        self.session_id = 0
        # Description of the experiment
        self.experiment_description = 'Experiment 1'
    
    # Get path roi file
    def get_roi_path(self):
        return os.path.join(self.exp_data_folder, self.roi_path)
    
    # Get path external data file
    def get_external_data_path(self):
        return os.path.join(self.exp_data_folder, self.external_data_path)

    # Get path training data file
    def get_training_data_path(self):
        return os.path.join(self.exp_data_folder, self.training_data_path)

# Utility params
# TODO: Consider asserting that this is indeed the prefix of the roi activity columns
roi_column_prefix = 'Mean'
