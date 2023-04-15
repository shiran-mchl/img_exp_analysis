# Class for holding the experiment results
import datetime
import pandas as pd


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
    
    def set_results(self, results: pd.DataFrame):
        self.results = results
    
    def set_training_data(self, training_data: pd.DataFrame):
        self.training_data = training_data
    
