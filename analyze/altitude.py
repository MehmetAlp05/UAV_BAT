
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

# File path (update accordingly)
output_file = "altitude/simulation_results_altitude.json"

# Function to read and parse JSON files
def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"The JSON file {file_path} contains invalid data.")
    return data if isinstance(data, list) else [data]

# Load data
runs = load_json(output_file)

# Organize data by UAV number
uav_groups = {}
for run in runs:
    uav_number = run["UAV_number"]
    if uav_number not in uav_groups:
        uav_groups[uav_number] = {"road_length": [], "uav_altitude": [], "success_ratio": []}
    
    uav_groups[uav_number]["road_length"].append(run["road_length"])
    uav_groups[uav_number]["uav_altitude"].append(run["uav_altitude"])
    uav_groups[uav_number]["success_ratio"].append(-run["best_fitness"])  # Negate for success ratio

# Plot each UAV number as a separate transparent surface
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection="3d")

colors = ["viridis", "plasma", "coolwarm", "magma", "cividis"]  # Different colormaps for UAVs

for i, (uav_number, data) in enumerate(uav_groups.items()):
    road_lengths = np.array(data["road_length"])
    uav_altitudes = np.array(data["uav_altitude"])
    success_ratios = np.array(data["success_ratio"])

    # Create grid for surface plot
    X, Y = np.meshgrid(np.linspace(min(road_lengths), max(road_lengths), 50), 
                        np.linspace(min(uav_altitudes), max(uav_altitudes), 50))
    
    Z = griddata((road_lengths, uav_altitudes), success_ratios, (X, Y), method="cubic")

    # Plot transparent surface
    surf = ax.plot_surface(X, Y, Z, cmap=colors[i % len(colors)], alpha=0.5, edgecolor="k", linewidth=0.2)

    # Add color bar
    #cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    #cbar.set_label(f"Success Ratio (UAVs={uav_number})")

# Labels
ax.set_title("Success Ratio vs. Road Length & UAV Altitude", fontsize=16)
ax.set_xlabel("Road Length", fontsize=12)
ax.set_ylabel("UAV Altitude", fontsize=12)
ax.set_zlabel("Success Ratio", fontsize=12)

# Show plot
plt.savefig("./altitude_comparison.png")  # Save the figure
plt.show()
