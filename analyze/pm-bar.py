import os
import json
import matplotlib.pyplot as plt
import numpy as np

# Paths to your JSON files
json_file_1 = "analyze/pm/pm-bat.json"  # First algorithm JSON file
json_file_2 = "analyze/pm/pm-pso.json"  # Second algorithm JSON file

# Function to load JSON
def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in {file_path}.")

# Load the data
data_1 = load_json(json_file_1)
data_2 = load_json(json_file_2)

# Combine both datasets
data = data_1 + data_2

# Extract data
algorithms = []
transmit_powers = []
uav_numbers = []
best_fitness_values = []

for entry in data:
    algorithm_name = "BA" if entry in data_1 else "PSO"
    algorithms.append(entry.get("algorithm", algorithm_name))
    transmit_powers.append(entry["transmission_power"])
    uav_numbers.append(entry["UAV_number"])
    best_fitness_values.append(-entry["best_fitness"])  # Convert to positive

# Convert to NumPy arrays
algorithms = np.array(algorithms)
transmit_powers = np.array(transmit_powers)
uav_numbers = np.array(uav_numbers)
best_fitness_values = np.array(best_fitness_values)

# Unique values
unique_algorithms = np.unique(algorithms)
unique_transmit_powers = np.unique(transmit_powers)
unique_uav_numbers = np.unique(uav_numbers)

# Create bar graph
fig, ax = plt.subplots(figsize=(12, 7))
bar_width = 0.15  # Adjust bar width for better visibility
colors = {uav: color for uav, color in zip(unique_uav_numbers, ["blue", "red", "green", "purple", "orange", "cyan"])}  # Assign colors per UAV
patterns = ["//", "\\"]  # Different patterns for algorithms

x_indices = np.arange(len(unique_transmit_powers))
offset = 0

for alg_idx, algorithm in enumerate(unique_algorithms):
    for j, uav in enumerate(unique_uav_numbers):
        mask = (uav_numbers == uav) & (algorithms == algorithm)
        avg_fitness_per_power = [
            np.mean(best_fitness_values[(mask) & (transmit_powers == power)])
            for power in unique_transmit_powers
        ]
        ax.bar(x_indices + offset, avg_fitness_per_power, bar_width,
               color=colors[uav], hatch=patterns[alg_idx],
               label=f"{algorithm} - {uav} UAVs")
        offset += bar_width

# Labels and title
ax.set_xlabel("Transmission Power (dBm)", fontsize=16)
ax.set_ylabel("Success Probability", fontsize=16)
ax.set_xticks(x_indices + (len(unique_algorithms) * len(unique_uav_numbers) / 2) * bar_width)
ax.set_xticklabels(unique_transmit_powers)
ax.legend(fontsize=10, title="Algorithm & UAVs", loc="upper left")
ax.grid(axis="y", linestyle="--", alpha=0.7)
ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=10))

# Save and show plot
plt.tight_layout()
plt.savefig("analyze/pm/success_probability_vs_transmit_power.png", bbox_inches='tight')
plt.show()