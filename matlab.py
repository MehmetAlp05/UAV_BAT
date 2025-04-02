import os
import json
import scipy.io

# File paths for the three algorithms
output_file_algo1 = "analyze/datarate/bat test.json"
output_file_algo2 = "analyze/datarate/bat test.json"
output_file_algo3 = "analyze/datarate/pso test.json"

def load_json(file_path):
    """Loads JSON data from a given file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"The JSON file {file_path} contains invalid data.")
    return data["runs"] if isinstance(data, dict) and "runs" in data else data

# Load JSON data
runs_algo1 = load_json(output_file_algo1)
runs_algo2 = load_json(output_file_algo2)
runs_algo3 = load_json(output_file_algo3)

def extract_data(runs):
    """Extracts relevant fields for MATLAB."""
    data_rates, uav_numbers, best_fitness_values = [], [], []
    for run in runs:
        data_rate = run.get("data_rate(mbit)")
        uav_number = run.get("UAV_number")
        best_fitness = run.get("best_fitness")
        if data_rate is not None and uav_number is not None and best_fitness is not None:
            data_rates.append(data_rate)
            uav_numbers.append(int(uav_number))
            best_fitness_values.append(-best_fitness)  # Convert to success probability
    return data_rates, uav_numbers, best_fitness_values

# Extract data for each algorithm
data_rates1, uav_numbers1, best_fitness1 = extract_data(runs_algo1)
data_rates2, uav_numbers2, best_fitness2 = extract_data(runs_algo2)
data_rates3, uav_numbers3, best_fitness3 = extract_data(runs_algo3)

# Save data to a .mat file for MATLAB
scipy.io.savemat("data_for_matlab.mat", {
    "data_rates1": data_rates1,
    "uav_numbers1": uav_numbers1,
    "best_fitness1": best_fitness1,
    "data_rates2": data_rates2,
    "uav_numbers2": uav_numbers2,
    "best_fitness2": best_fitness2,
    "data_rates3": data_rates3,
    "uav_numbers3": uav_numbers3,
    "best_fitness3": best_fitness3
})

print("Data saved to data_for_matlab.mat")
