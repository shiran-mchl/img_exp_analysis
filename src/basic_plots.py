# Draw basic plots using the experiment class

import matplotlib.pyplot as plt
import numpy as np
from experiment import Experiment
from exp_builder import build_experiment_from_config
from exp_config import ConfigParams

# TODO: Maybe all plot functions should be wrapped in a PlotBuilder class.

# A function that gets an experiment and plots the activity of all rois in a given range of trials. 
# Add a vertical line after 2.5 seconds.
def plot_activity_of_all_rois_in_trial(exp: Experiment, trial_start: int, trial_end: int = None):
    if trial_end is None:
        trial_end = trial_start
    for i in range(exp.get_number_of_rois()):
        activity = []
        # TODO: Maybe this should be a function in Experiment class.
        for j in range(trial_start, trial_end+1):
            activity.extend(exp.get_roi_activity_by_trial(i+1, j))
        plt.plot(activity)
    # Add a vertical line after 2.5 seconds
    plt.axvline(x=ConfigParams().roi_sampling_rate*2.5, color='r')
    if trial_start == trial_end:
        plt.title(f'Activity of all rois in trial {trial_start}')
    else:
        plt.title(f'Activity of all rois in trials {trial_start}-{trial_end}')
    plt.xlabel('Time (1/20 second)')
    plt.ylabel('Activity')

if __name__ == '__main__':
    # Create experiment builder
    exp = build_experiment_from_config(ConfigParams())
    plt.figure()
    # Plot the activity of all rois in all 0 and 7
    plt.subplot(2, 2, 1)
    plot_activity_of_all_rois_in_trial(exp, 7)
    plt.subplot(2, 2, 2)
    plot_activity_of_all_rois_in_trial(exp, 8)
    plt.subplot(2, 2, 3)
    plot_activity_of_all_rois_in_trial(exp, 9)
    plt.subplot(2, 2, 4)
    plot_activity_of_all_rois_in_trial(exp, 7,9)
    plt.show()