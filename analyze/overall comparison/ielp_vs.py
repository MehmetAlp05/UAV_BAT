import os
import json
import matplotlib.pyplot as plt
import numpy as np

# File paths for the two algorithms
output_file_algo1 = "bat_results/final_results.json"
output_file_algo2 = "IE-LP_results/final_results.json"

# Function to read and parse JSON files
def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"The JSON file {file_path} contains invalid data.")
    # Determine if the data is a list of runs or a dictionary with a "runs" key
    if isinstance(data, dict) and "runs" in data:
        return data["runs"]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError(f"Unexpected JSON structure in {file_path}. Unable to parse runs.")

# Load data for both algorithms
runs_algo1 = load_json(output_file_algo1)
runs_algo2 = load_json(output_file_algo2)

# Extract data for plotting
def extract_data(runs):
    data_rates = []
    uav_numbers = []
    best_fitness_values = []
    for run in runs:
        data_rate = run.get("data_rate(mbit)", None)
        uav_number = run.get("UAV_number", None)
        best_fitness = run.get("best_fitness", None)
        if data_rate is not None and uav_number is not None and best_fitness is not None:
            data_rates.append(data_rate)
            uav_numbers.append(int(uav_number))  # Ensure UAV numbers are integers
            best_fitness_values.append(-best_fitness)  # Multiply fitness by -1
    return np.array(data_rates), np.array(uav_numbers), np.array(best_fitness_values)

data_rates_algo1, uav_numbers_algo1, best_fitness_values_algo1 = extract_data(runs_algo1)
data_rates_algo2, uav_numbers_algo2, best_fitness_values_algo2 = extract_data(runs_algo2)

# Ensure there is data to plot
if len(data_rates_algo1) == 0 or len(data_rates_algo2) == 0:
    raise ValueError("No valid data found in the JSON files for plotting.")

# Define custom colors for data rates and UAV numbers
custom_colors_data_rate = {
    6000000: "red",  # Data Rate 12 Mbit
    12000000: "blue", # Data Rate 24 Mbit
    18000000: "green" # Data Rate 48 Mbit
}

custom_colors_uav_number = {
    1: "brown",   # UAV Number 1
    2: "goldenrod",   # UAV Number 3
    3: "darkgreen",     # UAV Number 5
    4: "dodgerblue",  # UAV Number 10
    5: "indigo"  # UAV Number 10
}

# Define line styles for algorithms
line_styles = {
    "Bat": "solid",
    "IE-LP": "dashed"
}
markers = {
    "Bat": "o",  # Circle marker
    "IE-LP": "s"   # Square marker
}
# Create a figure with subplots
fig = plt.figure(figsize=(16, 8))

# Subplot 1: Fitness vs. UAV Number (2D)
ax1 = fig.add_subplot(121)
unique_data_rates = np.unique(np.concatenate([data_rates_algo1, data_rates_algo2]))
for rate in unique_data_rates:
    for data_rates, uav_numbers, best_fitness_values, label in [
        (data_rates_algo1, uav_numbers_algo1, best_fitness_values_algo1, "Bat"),
        (data_rates_algo2, uav_numbers_algo2, best_fitness_values_algo2, "IE-LP"),
    ]:
        mask = data_rates == rate
        sorted_indices = np.argsort(uav_numbers[mask])
        sorted_uav = uav_numbers[mask][sorted_indices]
        sorted_fitness = best_fitness_values[mask][sorted_indices]
        color = custom_colors_data_rate.get(rate, "black")  # Default to black if rate is not in the dictionary
        ax1.scatter(sorted_uav, sorted_fitness, label=f"{label} ( {rate/10e5:.1f} Mbit)", s=50, color=color,marker=markers[label])
        ax1.plot(sorted_uav, sorted_fitness, linestyle=line_styles[label], alpha=0.7, color=color)

ax1.set_title("Success Ratio vs. UAV Number", fontsize=28)
ax1.set_xlabel("UAV Number", fontsize=24)
ax1.set_ylabel("Success Ratio", fontsize=24)
ax1.grid(True)
ax1.legend(fontsize=16)

# Subplot 2: Fitness vs. Data Rate (2D)
ax2 = fig.add_subplot(122)
unique_uav_numbers = np.unique(np.concatenate([uav_numbers_algo1, uav_numbers_algo2]))
for uav in unique_uav_numbers:
    for data_rates, uav_numbers, best_fitness_values, label in [
        (data_rates_algo1, uav_numbers_algo1, best_fitness_values_algo1, "Bat"),
        (data_rates_algo2, uav_numbers_algo2, best_fitness_values_algo2, "IE-LP"),
    ]:
        mask = uav_numbers == uav
        sorted_indices = np.argsort(data_rates[mask])
        sorted_data_rates = data_rates[mask][sorted_indices]
        sorted_fitness = best_fitness_values[mask][sorted_indices]
        color = custom_colors_uav_number.get(uav, "black")  # Default to black if UAV is not in the dictionary
        ax2.scatter(sorted_data_rates, sorted_fitness, label=f"{label} (UAV {uav})", s=50, color=color,marker=markers[label])
        ax2.plot(sorted_data_rates, sorted_fitness, linestyle=line_styles[label], alpha=0.7, color=color)

ax2.set_title("Success Ratio vs. Data Rate", fontsize=28)
ax2.set_xlabel("Data Rate (Mbit)", fontsize=24)
ax2.set_ylabel("Success Ratio", fontsize=24)
ax2.grid(True)
ax2.legend(fontsize=16)

# Adjust layout and show the plots
plt.tight_layout()
plt.savefig("./ielp_vs.png")  # Save the figure
plt.show()