import json

# Load JSON data
with open("analyze/cpu/cpu-pso.json", "r") as file:
    data = json.load(file)

# Initialize lists for each UAV number
UAV_1 = []
UAV_2 = []
UAV_3 = []

# Sort data into respective UAV lists
for entry in data:
    if entry["UAV_number"] == 1:
        UAV_1.append(str(entry["best_fitness"]))
    elif entry["UAV_number"] == 2:
        UAV_2.append(str(entry["best_fitness"]))
    elif entry["UAV_number"] == 3:
        UAV_3.append(str(entry["best_fitness"]))

# Convert lists to MATLAB array format
UAV_1_matlab = "UAV_1 = [" + ", ".join(UAV_1) + "]";
UAV_2_matlab = "UAV_2 = [" + ", ".join(UAV_2) + "]";
UAV_3_matlab = "UAV_3 = [" + ", ".join(UAV_3) + "]";

# Save to MATLAB script file
with open("uav_data.m", "w") as file:
    file.write(UAV_1_matlab + "\n\n" + UAV_2_matlab + "\n\n" + UAV_3_matlab)

print("MATLAB script 'uav_data.m' generated successfully!")