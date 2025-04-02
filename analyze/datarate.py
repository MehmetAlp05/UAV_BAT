import os
import json
import matplotlib.pyplot as plt
import numpy as np

# File paths for the three algorithms
output_file_algo1 = "analyze/datarate/bat test.json"
output_file_algo2 = "analyze/overall/IE-LP_results/final_results.json"
output_file_algo3 = "analyze/datarate/simulation_results_data_rate_6.json"

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

# Define colors for data rates
custom_colors_rate_number = {6: "blue", 12: "red", 18: "green"}
# Define markers and line styles for algorithms
line_styles = {"BA": "solid", "IE-LP": "dashed", "PSO": "dotted"}
markers = {"BA": "o", "IE-LP": "s", "PSO": "x"}

fig, ax = plt.subplots(figsize=(8, 6))

unique_data_rates = np.unique(np.concatenate([data_rates_algo1, data_rates_algo2, data_rates_algo3]))
legend_lines = []  # Stores line legend handles
legend_markers = []  # Stores marker + line legend handles

for rate in unique_data_rates:
    color = custom_colors_rate_number.get(rate / 10e5, "black")
    line, = ax.plot([], [], color=color, linestyle="-", label=f"{rate / 10e5:.1f} Mbit")  # Empty plot for legend
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
    
    for rate in unique_data_rates:
        mask = data_rates == rate
        sorted_indices = np.argsort(uav_numbers[mask])
        sorted_uav = uav_numbers[mask][sorted_indices]
        sorted_fitness = best_fitness_values[mask][sorted_indices]
        color = custom_colors_rate_number.get(rate / 10e5, "black")

        ax.scatter(sorted_uav, sorted_fitness, s=50, color=color, marker=marker)
        ax.plot(sorted_uav, sorted_fitness, linestyle=linestyle, alpha=0.7, color=color)

ax.set_xlabel("UAV Number", fontsize=16)
ax.set_ylabel("Success Probability", fontsize=16)
ax.grid(True)

# Create separate legends
legend1 = ax.legend(handles=legend_lines, title="Data Rate", loc="lower left", fontsize=12)
ax.add_artist(legend1)  # Add the first legend manually

legend2 = ax.legend(handles=legend_markers, title="Algorithm", loc="lower right", fontsize=12)

plt.tight_layout()
plt.savefig("analyze/datarate/success_ratio_vs_uav_number.png")
plt.show()