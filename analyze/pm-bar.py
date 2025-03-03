import os
import json
import matplotlib.pyplot as plt
import numpy as np

# Path to your JSON file
json_file = "analyze/pm/pm-bat.json"  # Change this to your actual JSON file path

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
uav_numbers = []
best_fitness_values = []
data_rates = []

for entry in data:
    uav_numbers.append(entry["UAV_number"])
    best_fitness_values.append(-entry["best_fitness"])  # Multiply by -1
    data_rates.append(entry["data_rate(mbit)"])  # Extract data rate

# Convert to NumPy arrays
uav_numbers = np.array(uav_numbers)
best_fitness_values = np.array(best_fitness_values)
data_rates = np.array(data_rates)

# Unique values
unique_uav_numbers = np.unique(uav_numbers)
unique_data_rates = np.unique(data_rates)

# Create bar graph
fig, ax = plt.subplots(figsize=(12, 7))
bar_width = 0.2  # Width of bars
colors = ["blue", "red", "green"]  # Colors for different data rates

x_indices = np.arange(len(unique_uav_numbers))
offset = 0

for j, data_rate in enumerate(unique_data_rates):
    mask = data_rates == data_rate
    avg_fitness_per_uav = [
        np.mean(best_fitness_values[(mask) & (uav_numbers == uav)])
        for uav in unique_uav_numbers
    ]
    ax.bar(x_indices + offset, avg_fitness_per_uav, bar_width, 
           color=colors[j % len(colors)], label=f"{data_rate / 1e6} Mbps")
    offset += bar_width

# Labels and title
ax.set_xlabel("Number of UAVs", fontsize=16)
ax.set_ylabel("Success Probability", fontsize=16)
#ax.set_title("Success Probability vs. Number of UAVs for Different Data Rates", fontsize=18)
ax.set_xticks(x_indices + (len(unique_data_rates) / 2) * bar_width)
ax.set_xticklabels(unique_uav_numbers)
ax.legend(fontsize=10, title="Data Rate", loc="upper left", bbox_to_anchor=(1, 1))
ax.grid(axis="y", linestyle="--", alpha=0.7)
ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=10))  # Increase y-axis detail

# Save and show plot
plt.tight_layout()
plt.savefig("analyze/pm/success_probability_bar_chart.png", bbox_inches='tight')
plt.show()