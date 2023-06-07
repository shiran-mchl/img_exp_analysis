class ConfigParams:
    def __init__(self):
        # exp data folder
        self.exp_data_folder = 'exp_data'
        # tunnel ID
        tunnel_id = 'pinkPort'
        # training day
        training_day = '2023-05-30'
        # trial type
        trial_type = 'Reward'
        # path to training data file
        self.training_data_path = 'pinkPort_2023-05-30'
        # trained mice
        self.trained_mice = ['R13', 'R14', 'R15', 'R17']
        # Description of the experiment
        self.experiment_description = 'test training data'