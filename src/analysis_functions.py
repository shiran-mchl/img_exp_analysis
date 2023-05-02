import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from experiment import Experiment
from exp_builder import build_experiment_from_config
from exp_config import ConfigParams

# A function that gets external data results from Experiment and plots it.
def plot_external_data_results(exp: Experiment):
    # Get the external data results
    external_data_results = exp.get_external_data_results()
    # Plot the results
    plt.plot(external_data_results['E-phys'])
    plt.plot(external_data_results['Stim. Marker'])
    plt.title('External data results')
    plt.xlabel('Time')
    plt.ylabel('Data')
    plt.show()



if __name__ == '__main__':
    # Create experiment builder
    exp = build_experiment_from_config(ConfigParams())
    # Plot the external data results
    plot_external_data_results(exp)
    # jump_locations = get_locations_of_differences(exp.get_external_data_results()['Stim. Marker'].values, 1, True)
    # print(jump_locations)
    # jump_locations = get_locations_of_differences(exp.get_external_data_results()['Stim. Marker'].values, -1, False)
    # print(jump_locations)

