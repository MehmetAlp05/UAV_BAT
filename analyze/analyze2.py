import os
import json
import matplotlib.pyplot as plt
import numpy as np

# File path
output_file = "simulation_results/final_results.json"

# Check if the file exists
if not os.path.exists(output_file):
    raise FileNotFoundError(f"The file {output_file} does not exist.")

# Read the JSON data
with open(output_file, "r") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("The JSON file contains invalid data.")

# Determine if the data is a list of runs or a dictionary with a "runs" key
if isinstance(data, dict) and "runs" in data:
    runs = data["runs"]
elif isinstance(data, list):
    runs = data
else:
    raise ValueError("Unexpected JSON structure. Unable to parse runs.")

# Extract data for plotting
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
        best_fitness_values.append(-1 * best_fitness)  # Multiply fitness by -1

# Ensure there is data to plot
if not data_rates or not uav_numbers or not best_fitness_values:
    raise ValueError("No valid data found in the JSON file for plotting.")

# Convert lists to numpy arrays for easier indexing
data_rates = np.array(data_rates)
uav_numbers = np.array(uav_numbers)
best_fitness_values = np.array(best_fitness_values)

# Create a figure with subplots
fig = plt.figure(figsize=(16, 8))

# Subplot 1: Fitness vs. UAV Number (2D) - Different colors for Data Rates
ax1 = fig.add_subplot(121)
unique_data_rates = np.unique(data_rates)
for rate in unique_data_rates:
    mask = data_rates == rate
    # Sort by UAV number for left-to-right order
    sorted_indices = np.argsort(uav_numbers[mask])
    sorted_uav = uav_numbers[mask][sorted_indices]
    sorted_fitness = best_fitness_values[mask][sorted_indices]
    # Scatter plot
    ax1.scatter(sorted_uav, sorted_fitness, label=f"Data Rate {rate/10e5:.1f} Mbit", s=50)
    # Line plot
    ax1.plot(sorted_uav, sorted_fitness, linestyle='-', alpha=0.7)
ax1.set_title("Fitness vs. UAV Number", fontsize=14)
ax1.set_xlabel("UAV Number", fontsize=12)
ax1.set_ylabel("Best Fitness", fontsize=12)
ax1.grid(True)
ax1.legend(fontsize=8)

# Subplot 2: Fitness vs. Data Rate (2D) - Different colors for UAV Numbers
ax2 = fig.add_subplot(122)
unique_uav_numbers = np.unique(uav_numbers)
for uav in unique_uav_numbers:
    mask = uav_numbers == uav
    # Sort by Data Rate for left-to-right order
    sorted_indices = np.argsort(data_rates[mask])
    sorted_data_rates = data_rates[mask][sorted_indices]
    sorted_fitness = best_fitness_values[mask][sorted_indices]
    # Scatter plot
    ax2.scatter(sorted_data_rates, sorted_fitness, label=f"UAV {uav}", s=50)
    # Line plot
    ax2.plot(sorted_data_rates, sorted_fitness, linestyle='-', alpha=0.7)
ax2.set_title("Fitness vs. Data Rate", fontsize=14)
ax2.set_xlabel("Data Rate (Mbit)", fontsize=12)
ax2.set_ylabel("Best Fitness", fontsize=12)
ax2.grid(True)
ax2.legend(fontsize=8)

# Adjust layout and show the plots
plt.tight_layout()
plt.savefig("./output.svg")  # Save the figure
plt.show()
