import os
import json
import matplotlib.pyplot as plt
import numpy as np

# File paths (Update these to your actual file locations)
output_file_algo1 = "pm/pm-bat.json"  # First algorithm (BA)
output_file_algo2 = "pm/simulation_results_pm.json"  # Second algorithm (PSO)

# Function to read and parse JSON files
def load_json(file_path, algo_label):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"The JSON file {file_path} contains invalid data.")
    
    return [(run, algo_label) for run in data] if isinstance(data, list) else [(data, algo_label)]

# Load data
runs_algo1 = load_json(output_file_algo1, "algo1")  # BA
runs_algo2 = load_json(output_file_algo2, "algo2")  # PSO

# Combine both datasets
all_runs = runs_algo1 + runs_algo2

# Extract data grouped by UAV number and algorithm
uav_data = {}
for run, algo in all_runs:
    uav_num = run["UAV_number"]
    tx_power = run["transmission_power"]
    success_ratio = -run["best_fitness"]  # Negate fitness to get success ratio
    
    if uav_num not in uav_data:
        uav_data[uav_num] = {"algo1": {"transmission_power": [], "success_ratio": []}, 
                             "algo2": {"transmission_power": [], "success_ratio": []}}
    
    uav_data[uav_num][algo]["transmission_power"].append(tx_power)
    uav_data[uav_num][algo]["success_ratio"].append(success_ratio)

# Create a figure
fig, ax = plt.subplots(figsize=(10, 6))

# Define colors for different UAV numbers
colors = ["blue", "red", "green", "orange", "purple"]
uav_legend_handles = []  # To store UAV legend handles
algo_legend_handles = []  # To store algorithm legend handles

# Plot data for each UAV number, distinguishing algorithms by line style
for i, (uav_num, data) in enumerate(sorted(uav_data.items())):
    color = colors[i % len(colors)]
    uav_label = f"UAV {uav_num}"
    
    if i == 0:  # Create algorithm legend only once
        algo_legend_handles.append(ax.plot([], [], linestyle="-", color="black", label="BA")[0])
        algo_legend_handles.append(ax.plot([], [], linestyle="--", color="black", label="PSO")[0])

    uav_legend_handles.append(ax.plot([], [], color=color, label=uav_label)[0])  # UAV color legend
    
    for algo, linestyle in [("algo1", "-"), ("algo2", "--")]:  # Solid for BA, dashed for PSO
        if len(data[algo]["transmission_power"]) > 0:  # Check if there's data for this UAV & algorithm
            sorted_indices = np.argsort(data[algo]["transmission_power"])
            tx_power_sorted = np.array(data[algo]["transmission_power"])[sorted_indices]
            success_ratio_sorted = np.array(data[algo]["success_ratio"])[sorted_indices]
            
            ax.plot(tx_power_sorted, success_ratio_sorted, marker="o", linestyle=linestyle, 
                    color=color)

# Set titles and labels
ax.set_title("Success Ratio vs. Transmission Power", fontsize=20)
ax.set_xlabel("Transmission Power (dBm)", fontsize=16)
ax.set_ylabel("Success Ratio", fontsize=16)
ax.grid(True)

# Add separate legends
legend1 = ax.legend(handles=uav_legend_handles, title="UAV Number", loc="upper left", fontsize=12)
legend2 = ax.legend(handles=algo_legend_handles, title="Algorithm", loc="lower right", fontsize=12)

ax.add_artist(legend1)  # Ensure both legends appear

# Adjust layout and show the plot
plt.tight_layout()
plt.savefig("./transmission_power_comparison.png")  # Save the figure
plt.show()
