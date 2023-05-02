# A function that gets a list of numbers and a list the locations where the difference between the numbers is greater or smaller
# than a threshold. The function also gets a boolean indicating if we are looking for greater or smaller than the threshold.
def get_locations_of_differences(numbers: list, threshold: float, greater_than: bool):
    if not greater_than:
        threshold = -threshold
    # Create a list of the differences between the numbers
    differences = [numbers[i+1] - numbers[i] for i in range(len(numbers)-1)]
    # Create a list of the locations where the difference is greater or smaller than the threshold
    if greater_than:
        locations = [i+1 for i in range(len(differences)) if differences[i] > threshold]
    else:
        locations = [i+1 for i in range(len(differences)) if differences[i] < threshold]
    return locations
