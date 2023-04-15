# Draw basic plots using the experiment class

import matplotlib.pyplot as plt
import numpy as np
from experiment import Experiment
from exp_builder import build_experiment_from_config
from exp_config import ConfigParams

# TODO: Maybe all plot functions should be wrapped in a PlotBuilder class.

# A function that gets an experiment and plots the activity of all rois in a specific trial. 
# Add a vertical line after 2.5 seconds.
def plot_activity_of_all_rois_in_trial(exp: Experiment, trial_number: int):
    for i in range(exp.get_number_of_rois()):
        plt.plot(exp.get_roi_activity_by_trial(i+1, trial_number))
    # Add a vertical line after 2.5 seconds
    plt.axvline(x=ConfigParams().roi_sampling_rate*2.5, color='r')
    plt.title(f'Activity of all rois in trial {trial_number}')
    plt.xlabel('Time (1/20 second)')
    plt.ylabel('Activity')
    plt.show()
    

if __name__ == '__main__':
    # Create experiment builder
    exp = build_experiment_from_config(ConfigParams())
    # Plot the activity of all rois in all 0 and 7
    plot_activity_of_all_rois_in_trial(exp, 0)
    plot_activity_of_all_rois_in_trial(exp, 7)
