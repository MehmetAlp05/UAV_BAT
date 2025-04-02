import json
from collections import defaultdict

def normalize_json(input_file, output_file):
    # Load JSON data
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Dictionary to store grouped results
    grouped_data = defaultdict(lambda: {"total_fitness": 0, "count": 0})

    # Process each entry
    for entry in data:
        # Extract key excluding `best_fitness` and `best_position`
        key = tuple((k, v) for k, v in entry.items() if k not in ["best_fitness", "best_position"])
        
        # Update grouped data
        grouped_data[key]["total_fitness"] += entry["best_fitness"]
        grouped_data[key]["count"] += 1

    # Create the normalized result
    normalized_data = []
    for key, value in grouped_data.items():
        avg_fitness = value["total_fitness"] / value["count"]
        normalized_entry = dict(key)
        normalized_entry["best_fitness"] = avg_fitness
        normalized_data.append(normalized_entry)

    # Save the normalized data back to JSON
    with open(output_file, 'w') as f:
        json.dump(normalized_data, f, indent=4)

# Example usage
input="pso_results/final_results.json"
output="pso_results/normalized_output.json"
normalize_json(input, output)
