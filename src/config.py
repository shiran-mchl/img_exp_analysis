import os

class ConfigParams:
    def __init__(self):
        # exp data folder
        self.exp_data_folder = 'exp_data'
        # Path to roi file
        self.roi_path = '02_stable_Results.csv'
        self.roi_sampling_rate = 20
        # path to external data file
        self.external_data_path = 'data_user_input.csv'
        # TODO: Verify external data sampling rate
        self.external_data_sampling_rate = 1200
        # path to training data file
        self.training_data_path = 'TrainingBox4_2022-11-02.csv'
    
    # Get path roi file
    def get_roi_path(self):
        return os.path.join(self.exp_data_folder, self.roi_path)
    
    # Get path external data file
    def get_external_data_path(self):
        return os.path.join(self.exp_data_folder, self.external_data_path)

    # Get path training data file
    def get_training_data_path(self):
        return os.path.join(self.exp_data_folder, self.training_data_path)
    