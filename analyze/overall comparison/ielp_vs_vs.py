import os
import json
import matplotlib.pyplot as plt
import numpy as np

# File paths for the three algorithms
output_file_algo1 = "./bat_results/final_results.json"  # Algorithm 1
output_file_algo2 = "./IE-LP_results/final_results.json"       # Algorithm 2
output_file_algo3 = "./pso/final_results.json"  # Algorithm 3

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

# Load data for all three algorithms
runs_algo1 = load_json(output_file_algo1)
runs_algo2 = load_json(output_file_algo2)
runs_algo3 = load_json(output_file_algo3)

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
data_rates_algo3, uav_numbers_algo3, best_fitness_values_algo3 = extract_data(runs_algo3)

# Ensure there is data to plot
if len(data_rates_algo1) == 0 or len(data_rates_algo2) == 0 or len(data_rates_algo3) == 0:
    raise ValueError("No valid data found in the JSON files for plotting.")

# Define custom colors for UAV numbers
custom_colors_uav_number = {
    1: "brown",        # UAV Number 1
    2: "goldenrod",    # UAV Number 3
    3: "darkgreen",    # UAV Number 5
    4: "dodgerblue",   # UAV Number 10
    5: "indigo"        # UAV Number 10
}
custom_colors_rate_number = {
    6: "brown",        # UAV Number 1
    12: "goldenrod",    # UAV Number 3
    18: "darkgreen",    # UAV Number 5

}

# Define line styles and markers for algorithms
line_styles = {
    "Bat": "solid",
    "IE-LP": "dashed",
    "pso": "dotted"
}
markers = {
    "Bat": "o",             # Circle marker
    "IE-LP": "s",           # Square marker
    "pso": "x"    # Cross marker
}

# Create a figure with subplots
fig = plt.figure(figsize=(16, 8))

# Subplot 1: Fitness vs. UAV Number (2D)
ax1 = fig.add_subplot(121)
unique_data_rates = np.unique(np.concatenate([data_rates_algo1, data_rates_algo2, data_rates_algo3]))
for rate in unique_data_rates:
    for data_rates, uav_numbers, best_fitness_values, label in [
        (data_rates_algo1, uav_numbers_algo1, best_fitness_values_algo1, "Bat"),
        (data_rates_algo2, uav_numbers_algo2, best_fitness_values_algo2, "IE-LP"),
        (data_rates_algo3, uav_numbers_algo3, best_fitness_values_algo3, "pso"),
    ]:
        mask = data_rates == rate
        sorted_indices = np.argsort(uav_numbers[mask])
        sorted_uav = uav_numbers[mask][sorted_indices]
        sorted_fitness = best_fitness_values[mask][sorted_indices]
        print(rate/10e5)
        color = custom_colors_rate_number.get(rate/10e5, "black")  # Default to black if UAV is not in the dictionary
        ax1.scatter(sorted_uav, sorted_fitness, label=f"{label} ({rate/10e5:.1f} Mbit)",color=color, s=50, marker=markers[label])
        ax1.plot(sorted_uav, sorted_fitness, linestyle=line_styles[label], alpha=0.7,color=color)

ax1.set_title("Success Ratio vs. UAV Number", fontsize=28)
ax1.set_xlabel("UAV Number", fontsize=24)
ax1.set_ylabel("Success Ratio", fontsize=24)
ax1.grid(True)
ax1.legend(fontsize=16)
# Separate legends for markers and colors
marker_legend = ax1.legend(
    [plt.Line2D([0], [0], color="black", marker=markers[algo], linestyle="", markersize=10) for algo in markers],
    [algo for algo in markers],
    loc="lower right",
    title="Algorithms",
    fontsize=12
)
ax1.add_artist(marker_legend)

color_legend = ax1.legend(
    [plt.Line2D([0], [0], color=color, marker="o", linestyle="", markersize=10) for color in custom_colors_rate_number.values()],
    [f"UAV {uav}" for uav in custom_colors_rate_number],
    loc="lower left",
    title="UAV Numbers",
    fontsize=12
)
# Subplot 2: Fitness vs. Data Rate (2D)
ax2 = fig.add_subplot(122)
unique_uav_numbers = np.unique(np.concatenate([uav_numbers_algo1, uav_numbers_algo2, uav_numbers_algo3]))
for uav in unique_uav_numbers:
    for data_rates, uav_numbers, best_fitness_values, label in [
        (data_rates_algo1, uav_numbers_algo1, best_fitness_values_algo1, "Bat"),
        (data_rates_algo2, uav_numbers_algo2, best_fitness_values_algo2, "IE-LP"),
        (data_rates_algo3, uav_numbers_algo3, best_fitness_values_algo3, "pso"),
    ]:
        mask = uav_numbers == uav
        sorted_indices = np.argsort(data_rates[mask])
        sorted_data_rates = data_rates[mask][sorted_indices]
        sorted_fitness = best_fitness_values[mask][sorted_indices]
        color = custom_colors_uav_number.get(uav, "black")  # Default to black if UAV is not in the dictionary
        ax2.scatter(sorted_data_rates, sorted_fitness, s=50, label=f"UAV {uav}", color=color, marker=markers[label])
        ax2.plot(sorted_data_rates, sorted_fitness, linestyle=line_styles[label], alpha=0.7, color=color)

ax2.set_title("Success Ratio vs. Data Rate", fontsize=28)
ax2.set_xlabel("Data Rate (Mbit)", fontsize=24)
ax2.set_ylabel("Success Ratio", fontsize=24)
ax2.grid(True)

# Separate legends for markers and colors
marker_legend = ax2.legend(
    [plt.Line2D([0], [0], color="black", marker=markers[algo], linestyle="", markersize=10) for algo in markers],
    [algo for algo in markers],
    loc="lower right",
    title="Algorithms",
    fontsize=12
)
ax2.add_artist(marker_legend)

color_legend = ax2.legend(
    [plt.Line2D([0], [0], color=color, marker="o", linestyle="", markersize=10) for color in custom_colors_uav_number.values()],
    [f"UAV {uav}" for uav in custom_colors_uav_number],
    loc="lower left",
    title="UAV Numbers",
    fontsize=12
)

# Adjust layout and show the plots
plt.tight_layout()
plt.savefig("./comparison_three_algorithms_separate_legends.png")  # Save the figure
plt.show()
