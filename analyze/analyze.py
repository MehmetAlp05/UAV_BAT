import os
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
        best_fitness_values.append(best_fitness)

# Ensure there is data to plot
if not data_rates or not uav_numbers or not best_fitness_values:
    raise ValueError("No valid data found in the JSON file for plotting.")

# Create a 3D scatter plot
fig = plt.figure(figsize=(16, 8))

# Subplot 1: Fitness vs. UAV Number (2D)
ax1 = fig.add_subplot(131)
ax1.scatter(uav_numbers, best_fitness_values, color="blue", label="Fitness vs. UAV Number", s=50)
ax1.set_title("Fitness vs. UAV Number", fontsize=14)
ax1.set_xlabel("UAV Number", fontsize=12)
ax1.set_ylabel("Best Fitness", fontsize=12)
ax1.grid(True)
ax1.legend(fontsize=10)

# Subplot 2: Fitness vs. Data Rate (2D)
ax2 = fig.add_subplot(132)
ax2.scatter(data_rates, best_fitness_values, color="green", label="Fitness vs. Data Rate", s=50)
ax2.set_title("Fitness vs. Data Rate", fontsize=14)
ax2.set_xlabel("Data Rate (Mbit)", fontsize=12)
ax2.set_ylabel("Best Fitness", fontsize=12)
ax2.grid(True)
ax2.legend(fontsize=10)

# Subplot 3: Fitness vs. Data Rate and UAV Number (3D)
ax3 = fig.add_subplot(133, projection='3d')
scatter = ax3.scatter(data_rates, uav_numbers, best_fitness_values, c=best_fitness_values, cmap="viridis", s=100)
ax3.set_title("Fitness vs. Data Rate and UAV Number", fontsize=14)
ax3.set_xlabel("Data Rate (Mbit)", fontsize=12)
ax3.set_ylabel("UAV Number", fontsize=12)
ax3.set_zlabel("Best Fitness", fontsize=12)

# Add a color bar for the 3D plot
cbar = plt.colorbar(scatter, ax=ax3, pad=0.1)
cbar.set_label("Best Fitness", fontsize=12)

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
