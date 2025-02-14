import os
import json
import matplotlib.pyplot as plt
import numpy as np

# Path to your JSON file
json_file = "simulation_results/normalized_output.json"  # Change this to your actual JSON file path

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
data = load_json(json_file)

# Extract data
transmission_powers = []
uav_numbers = []
best_fitness_values = []

for entry in data:
    transmission_powers.append(entry["transmission_power"])
    uav_numbers.append(entry["UAV_number"])
    best_fitness_values.append(-entry["best_fitness"])  # Multiply by -1

# Convert to NumPy arrays
transmission_powers = np.array(transmission_powers)
uav_numbers = np.array(uav_numbers)
best_fitness_values = np.array(best_fitness_values)

# Unique UAV numbers
unique_uav_numbers = np.unique(uav_numbers)

# Plot settings
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["blue", "red", "green", "orange", "purple", "brown"]
markers = ["o", "s", "x", "d", "^", "v"]

# Plot for each UAV number
for i, uav in enumerate(unique_uav_numbers):
    mask = uav_numbers == uav
    sorted_indices = np.argsort(transmission_powers[mask])
    sorted_transmission_powers = transmission_powers[mask][sorted_indices]
    sorted_fitness = best_fitness_values[mask][sorted_indices]

    ax.plot(sorted_transmission_powers, sorted_fitness, linestyle="solid", 
            color=colors[i % len(colors)], marker=markers[i % len(markers)], 
            label=f"UAV {uav}")

# Labels and title
ax.set_xlabel("Transmission Power (dBm)", fontsize=16)
ax.set_ylabel("Success Probability", fontsize=16)
ax.set_title("Success Probability vs. Transmission Power for Different UAV Numbers", fontsize=18)
ax.grid(True)
ax.legend(fontsize=12)

# Save and show plot
plt.tight_layout()
plt.savefig("success_probability_vs_transmission_power.png")
plt.show()
