from datetime import timedelta
from enum import Enum
from functools import reduce
import pandas as pd
import numpy as np
from config import ConfigParams
from utils import get_locations_of_differences

# A class for reading a training data file.
class TrainingData:
    def __init__(self):
        self.tunnel_id = ConfigParams.tunnel_id
        self.training_day = ConfigParams.training_day
        self.trial_type = ConfigParams.trial_type
        self.training_data = None
        self.training_data_path = ConfigParams.training_data_path
        

    # Read the training data file.
    def read_training_data(self):
        self.training_data = pd.read_csv(self.training_data_path)

