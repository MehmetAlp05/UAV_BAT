import os
import json
import matplotlib.pyplot as plt
import numpy as np

# File paths for the three algorithms
output_file_algo1 = "analyze/datarate/bat test.json"
output_file_algo2 = "analyze/datarate/ielp test.json"
output_file_algo3 = "analyze/datarate/pso test.json"

def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"The JSON file {file_path} contains invalid data.")
    return data["runs"] if isinstance(data, dict) and "runs" in data else data

runs_algo1 = load_json(output_file_algo1)
runs_algo2 = load_json(output_file_algo2)
runs_algo3 = load_json(output_file_algo3)

def extract_data(runs):
    data_rates, uav_numbers, best_fitness_values = [], [], []
    for run in runs:
        data_rate = run.get("data_rate(mbit)", None)
        uav_number = run.get("UAV_number", None)
        best_fitness = run.get("best_fitness", None)
        if data_rate is not None and uav_number is not None and best_fitness is not None:
            data_rates.append(data_rate)
            uav_numbers.append(int(uav_number))
            best_fitness_values.append(-best_fitness)
    return np.array(data_rates), np.array(uav_numbers), np.array(best_fitness_values)

data_rates_algo1, uav_numbers_algo1, best_fitness_values_algo1 = extract_data(runs_algo1)
data_rates_algo2, uav_numbers_algo2, best_fitness_values_algo2 = extract_data(runs_algo2)
data_rates_algo3, uav_numbers_algo3, best_fitness_values_algo3 = extract_data(runs_algo3)

# Define colors for UAV numbers
custom_colors_uav_number = {1: "blue", 2: "red", 3: "green", 4: "orange", 5: "purple"}
# Define markers and line styles for algorithms
line_styles = {"BA": "solid", "IE-LP": "dashed", "PSO": "dotted"}
markers = {"BA": "o", "IE-LP": "s", "PSO": "x"}

fig, ax = plt.subplots(figsize=(8, 6))

unique_uav_numbers = np.unique(np.concatenate([uav_numbers_algo1, uav_numbers_algo2, uav_numbers_algo3]))
legend_lines = []  # Stores line legend handles
legend_markers = []  # Stores marker + line legend handles

for uav in unique_uav_numbers:
    color = custom_colors_uav_number.get(uav, "black")
    line, = ax.plot([], [], color=color, linestyle="-", label=f" {uav}")  # Empty plot for legend
    legend_lines.append(line)

for data_rates, uav_numbers, best_fitness_values, label in [
    (data_rates_algo1, uav_numbers_algo1, best_fitness_values_algo1, "BA"),
    (data_rates_algo2, uav_numbers_algo2, best_fitness_values_algo2, "IE-LP"),
    (data_rates_algo3, uav_numbers_algo3, best_fitness_values_algo3, "PSO"),
]:
    marker = markers[label]
    linestyle = line_styles[label]
    
    # Create a dummy line with the corresponding linestyle and marker for legend
    dummy_line, = ax.plot([], [], linestyle=linestyle, color="black", marker=marker, label=label)
    legend_markers.append(dummy_line)
    
    for uav in unique_uav_numbers:
        mask = uav_numbers == uav
        sorted_indices = np.argsort(data_rates[mask])
        sorted_data_rates = data_rates[mask][sorted_indices]
        sorted_fitness = best_fitness_values[mask][sorted_indices]
        color = custom_colors_uav_number.get(uav, "black")
        
        ax.scatter(sorted_data_rates, sorted_fitness, s=50, color=color, marker=marker)
        ax.plot(sorted_data_rates, sorted_fitness, linestyle=linestyle, alpha=0.7, color=color)

ax.set_xlabel("Data Size (Mbit)", fontsize=16)
ax.set_ylabel("Success Probability", fontsize=16)
ax.grid(True)

# Create separate legends
legend1 = ax.legend(handles=legend_lines, title="Number of UAVs", loc="lower left", fontsize=12)
ax.add_artist(legend1)  # Add the first legend manually

legend2 = ax.legend(handles=legend_markers, title="Algorithm", loc="lower left", fontsize=12,bbox_to_anchor=(0, 0.20))

plt.tight_layout()
plt.savefig("analyze/datarate/success_ratio_vs_data_rate.png")
plt.show()