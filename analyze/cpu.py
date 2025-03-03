import json
import matplotlib.pyplot as plt

# Load data from two JSON files
file1 = "analyze/cpu/cpu-bat.json"  # BA algorithm
file2 = "analyze/cpu/cpu-pso.json"  # PSO algorithm

with open(file1, "r") as f:
    data1 = json.load(f)

with open(file2, "r") as f:
    data2 = json.load(f)

# Function to process data
def process_data(data):
    uav_data = {}
    for entry in data:
        uav_number = entry["UAV_number"]
        if uav_number not in uav_data:
            uav_data[uav_number] = {"computing_power": [], "best_fitness": []}
        uav_data[uav_number]["computing_power"].append(entry["computing_power"])
        uav_data[uav_number]["best_fitness"].append(-entry["best_fitness"])  # Reverse magnitude
    return uav_data

# Process both datasets
uav_data1 = process_data(data1)  # BA
uav_data2 = process_data(data2)  # PSO

# Plot settings
plt.figure(figsize=(10, 5))

# Colors and markers for distinction
colors = ["b", "r", "g", "m", "c", "y", "k"]
markers = ["o", "s"]  # Circle for BA, Square for PSO
linestyles = ["-", "--"]  # Solid for BA, Dashed for PSO

# Plot data
uav_numbers_legend = set()
for i, uav_number in enumerate(sorted(set(uav_data1.keys()).union(set(uav_data2.keys())))):
    if uav_number in uav_data1:
        plt.plot(
            uav_data1[uav_number]["computing_power"], uav_data1[uav_number]["best_fitness"], 
            marker=markers[0], linestyle=linestyles[0], color=colors[i % len(colors)],
            label=f"{uav_number}" if uav_number not in uav_numbers_legend else "_nolegend_"
        )
        uav_numbers_legend.add(uav_number)
    if uav_number in uav_data2:
        plt.plot(
            uav_data2[uav_number]["computing_power"], uav_data2[uav_number]["best_fitness"], 
            marker=markers[1], linestyle=linestyles[1], color=colors[i % len(colors)],
            label="_nolegend_"
        )

# Labels and grid
plt.xlabel("Computing Power")
plt.ylabel("Success Probability")
plt.xscale("log")  # Log scale for better visualization
plt.grid(True, which="both", linestyle="--", linewidth=0.7, alpha=0.7)

# Separate legends for UAV number and Algorithm (both in upper left)
legend1 = plt.legend(title="Number of UAVs", loc="upper left")
legend2 = plt.legend(handles=[
    plt.Line2D([0], [0], marker=markers[0], linestyle=linestyles[0], color="black", label="BA"),
    plt.Line2D([0], [0], marker=markers[1], linestyle=linestyles[1], color="black", label="PSO")
], title="Algorithm", loc="upper left", bbox_to_anchor=(0, 0.75))  # Positioned slightly below UAV legend
plt.gca().add_artist(legend1)

# Save figure
plt.savefig("analyze/cpu/computing_power.png", dpi=300, bbox_inches="tight")

# Show plot
plt.show()
