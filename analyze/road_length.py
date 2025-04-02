import os
import json
import matplotlib.pyplot as plt
import numpy as np

# File paths for both algorithms
output_file_algo1 = "analyze/road_length/road-bat2.json"  
#output_file_algo2 = "analyze/road_length/pso-roadd.json"  
output_file_algo2 = "analyze/road_length/road-ielp.json"  

# Function to read and parse JSON files
def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"The JSON file {file_path} contains invalid data.")
    return data["runs"] if isinstance(data, dict) and "runs" in data else data

# Load data for both algorithms
runs_algo1 = load_json(output_file_algo1)
runs_algo2 = load_json(output_file_algo2)

# Extract data for plotting
def extract_data(runs):
    road_lengths, best_fitness_values, uav_numbers = [], [], []
    for run in runs:
        road_length = run.get("road_length", None)
        best_fitness = run.get("best_fitness", None)
        uav_number = run.get("UAV_number", None)
        if road_length is not None and best_fitness is not None and uav_number is not None:
            road_lengths.append(road_length)
            best_fitness_values.append(-best_fitness)  # Multiply fitness by -1
            uav_numbers.append(int(uav_number))  # Convert UAV number to int
    return np.array(road_lengths), np.array(best_fitness_values), np.array(uav_numbers)

# Extract data for each algorithm
road_lengths_algo1, best_fitness_values_algo1, uav_numbers_algo1 = extract_data(runs_algo1)
road_lengths_algo2, best_fitness_values_algo2, uav_numbers_algo2 = extract_data(runs_algo2)

# Ensure there is data to plot
if len(road_lengths_algo1) == 0 or len(road_lengths_algo2) == 0:
    raise ValueError("No valid data found in the JSON files for plotting.")

# Define colors and styles for UAV numbers
uav_colors = {1: "blue", 2: "red", 3: "green"}  # Only 1, 2, 3 included
line_styles = {"BA": "solid", "PSO": "dashed"}
markers = {"BA": "o", "PSO": "s"}

fig, ax = plt.subplots(figsize=(10, 6))

# Unique UAV numbers (only 1, 2, 3)
unique_uav_numbers = [uav for uav in np.unique(np.concatenate([uav_numbers_algo1, uav_numbers_algo2])) if uav in uav_colors]

# Plot each UAV group separately for both algorithms
for uav in unique_uav_numbers:
    color = uav_colors.get(uav, "black")  # Default to black if UAV not in dict

    # Filter and sort data for BA (Bat Algorithm)
    mask1 = uav_numbers_algo1 == uav
    sorted_indices1 = np.argsort(road_lengths_algo1[mask1])
    sorted_road_lengths1 = road_lengths_algo1[mask1][sorted_indices1]
    sorted_fitness1 = best_fitness_values_algo1[mask1][sorted_indices1]

    # Filter and sort data for PSO (Particle Swarm Optimization)
    mask2 = uav_numbers_algo2 == uav
    sorted_indices2 = np.argsort(road_lengths_algo2[mask2])
    sorted_road_lengths2 = road_lengths_algo2[mask2][sorted_indices2]
    sorted_fitness2 = best_fitness_values_algo2[mask2][sorted_indices2]

    if len(sorted_road_lengths1) > 0:
        ax.plot(sorted_road_lengths1, sorted_fitness1, linestyle=line_styles["BA"], color=color, marker=markers["BA"], label=f"BA - UAV {uav}")
    if len(sorted_road_lengths2) > 0:
        ax.plot(sorted_road_lengths2, sorted_fitness2, linestyle=line_styles["PSO"], color=color, marker=markers["PSO"], label=f"PSO - UAV {uav}")

# Set labels and title
ax.set_xlabel("Road Length", fontsize=18)
ax.set_ylabel("Success Probability", fontsize=18)
ax.grid(True)

# Create separate legends for UAV colors and Algorithm markers
legend_uav = [plt.Line2D([0], [0], color=color, linestyle="-", label=f" {uav}") for uav, color in uav_colors.items()]
legend_algo = [plt.Line2D([0], [0], color="black", linestyle=line_styles[algo], marker=markers[algo], label=algo) for algo in line_styles]

legend1 = ax.legend(handles=legend_uav, title="Number of UAVs", loc="upper right", fontsize=12)
ax.add_artist(legend1)  # Add UAV legend manually

legend2 = ax.legend(handles=legend_algo, title="Algorithms", loc="upper right", fontsize=12,bbox_to_anchor=(1, 0.8))

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig("analyze/road_length/road-length-comparison.png")
plt.show()
