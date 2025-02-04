import os
import json
import matplotlib.pyplot as plt
import numpy as np

# File paths for both algorithms
output_file_algo1 = "road_length/bat_final_results.json"  # Change this to your file path
output_file_algo2 = "road_length/pso_final_results.json"  # Change this to your file path

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

# Load data for both algorithms
runs_algo1 = load_json(output_file_algo1)
runs_algo2 = load_json(output_file_algo2)

# Extract data for plotting
def extract_data(runs):
    road_lengths = []
    best_fitness_values = []
    for run in runs:
        road_length = run.get("road_length", None)
        best_fitness = run.get("best_fitness", None)
        if road_length is not None and best_fitness is not None:
            road_lengths.append(road_length)
            best_fitness_values.append(-best_fitness)  # Multiply fitness by -1
    return np.array(road_lengths), np.array(best_fitness_values)

road_lengths_algo1, best_fitness_values_algo1 = extract_data(runs_algo1)
road_lengths_algo2, best_fitness_values_algo2 = extract_data(runs_algo2)

# Debugging: Print the data to ensure it's loaded and structured correctly
print("Algorithm 1 - Road Lengths:", road_lengths_algo1)
print("Algorithm 1 - Best Fitness Values:", best_fitness_values_algo1)
print("Algorithm 2 - Road Lengths:", road_lengths_algo2)
print("Algorithm 2 - Best Fitness Values:", best_fitness_values_algo2)

# Ensure there is data to plot
if len(road_lengths_algo1) == 0 or len(road_lengths_algo2) == 0:
    raise ValueError("No valid data found in the JSON files for plotting.")

# Sort data by road lengths
sorted_indices_algo1 = np.argsort(road_lengths_algo1)
sorted_indices_algo2 = np.argsort(road_lengths_algo2)

road_lengths_algo1 = road_lengths_algo1[sorted_indices_algo1]
best_fitness_values_algo1 = best_fitness_values_algo1[sorted_indices_algo1]

road_lengths_algo2 = road_lengths_algo2[sorted_indices_algo2]
best_fitness_values_algo2 = best_fitness_values_algo2[sorted_indices_algo2]

# Create a figure
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)

# Define colors and styles
colors = ["blue", "red"]
line_styles = ["solid", "solid"]
labels = ["BA", "PSO"]

# Plot both algorithms
ax.plot(road_lengths_algo1, best_fitness_values_algo1, linestyle=line_styles[0], alpha=0.7, color=colors[0], label=labels[0])
ax.plot(road_lengths_algo2, best_fitness_values_algo2, linestyle=line_styles[1], alpha=0.7, color=colors[1], label=labels[1])

# Set titles and labels
ax.set_title("Success Ratio vs. Road Length", fontsize=24)
ax.set_xlabel("Road Length", fontsize=18)
ax.set_ylabel("Success Ratio", fontsize=18)
ax.grid(True)
ax.legend(fontsize=12)

# Adjust layout and show the plot
plt.tight_layout()
plt.savefig("./road-length-comparison.png")  # Save the figure
plt.show()
