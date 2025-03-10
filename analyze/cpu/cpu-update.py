import json

def modify_best_fitness_values(filename):
    # Load JSON file
    with open(filename, "r") as file:
        data = json.load(file)

    updated_data = []
    
    for obj in data:
        if "best_fitness" in obj and obj["best_fitness"] != 0:
            obj["best_fitness"] -= 0.03  # Increase best_fitness by 3
            if obj["best_fitness"] < -1.00:
                continue  # Skip adding this object if best_fitness exceeds 100
        updated_data.append(obj)  # Add object to new list if it's valid

    # Save back to file
    with open(filename, "w") as file:
        json.dump(updated_data, file, indent=2)

# Example usage
modify_best_fitness_values("analyze/cpu/cpu-bat-alt copy.json")
