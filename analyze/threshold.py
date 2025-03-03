import os
import json
import matplotlib.pyplot as plt
import numpy as np

# File path for the algorithm results
output_file_algo = "analyze/threshold/threshold.json"  # Change this to your file path

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

# Load data for the algorithm
runs_algo = load_json(output_file_algo)

# Extract data for plotting
def extract_data(runs):
    thresholds = []
    success_ratios = []
    for run in runs:
        threshold = run.get("threshold", None)
        success_ratio = run.get("success_ratio", None)
        if threshold is not None and success_ratio is not None:
            thresholds.append(threshold)
            success_ratios.append(success_ratio)
    return np.array(thresholds), np.array(success_ratios)

thresholds, success_ratios = extract_data(runs_algo)

# Ensure there is data to plot
if len(thresholds) == 0:
    raise ValueError("No valid data found in the JSON file for plotting.")

# Sort data by threshold values
sorted_indices = np.argsort(thresholds)
thresholds = thresholds[sorted_indices]
success_ratios = success_ratios[sorted_indices]

# Create a bar plot
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.05  # Set a fixed bar width
ax.bar(thresholds, success_ratios, width=bar_width, color="blue", alpha=0.7, label="Success Ratio")

# Set titles and labels
#ax.set_title("Success Ratio vs. Threshold", fontsize=24)
ax.set_xlabel("Threshold", fontsize=18)
ax.set_ylabel("Success Probability", fontsize=18)
ax.grid(axis="y", linestyle="--", alpha=0.7)
#ax.legend(fontsize=12)

# Adjust layout and show the plot
plt.xticks(thresholds)  # Ensure all threshold values are labeled on x-axis
plt.tight_layout()
plt.savefig("analyze/threshold/threshold-success-ratio.png")  # Save the figure
plt.show()
