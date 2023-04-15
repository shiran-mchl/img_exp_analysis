# Test the experiment builder and experiment classes:

from exp_builder import ExperimentBuilder, build_experiment_from_config
from exp_config import ConfigParams
from experiment import Experiment

# Create experiment builder
exp = build_experiment_from_config(ConfigParams())
assert exp.results.shape[0] == 16559
assert exp.results.shape[1] == 9

trial0_activity = exp.get_roi_activity_by_trial(1, 0)
assert trial0_activity.shape[0] == 2400
assert trial0_activity[0] == 73.806
assert trial0_activity[1199] == 0.334
trial2_activity = exp.get_roi_activity_by_trial(1, 2)
assert trial2_activity.shape[0] == 560
assert trial2_activity[0] == 163.583
assert trial2_activity[559] == 96.899
assert exp.get_number_of_trials() == 8
assert exp.get_number_of_rois() == 4
all_trial_activity = exp.get_trial_activity(0)
assert all_trial_activity.shape[0] == 2400
assert all_trial_activity.shape[1] == 4
assert all_trial_activity[0, 0] == 73.806
assert all_trial_activity[0, 1] == 54.741
print('All tests passed')

