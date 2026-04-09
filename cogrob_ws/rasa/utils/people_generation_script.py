import json
import random
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        # Convert NumPy integers to Python int
        if isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        # Convert NumPy floats to Python float
        if isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        # Convert NumPy arrays to Python lists
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        # Default behavior for other data types
        return super().default(obj)
    
def custom_dumps(data):
    """Custom JSON serialization that keeps `trajectory` lists aligned with other keys."""
    # Serialize the data to JSON with indentation
    json_str = json.dumps(data, cls=NpEncoder, indent=4)
    # Ensure `trajectory` lists are on a single line and aligned with other keys
    lines = json_str.splitlines()
    for i, line in enumerate(lines):
        if '"trajectory": [' in line:  # Detect the start of the trajectory list
            j = i
            while not lines[j].strip().endswith("]"):  # Find the end of the list
                j += 1
            # Combine all lines for this list into a single line
            combined = "".join(line.strip() for line in lines[i:j + 1])
            combined = combined.replace(", ", ",").replace("[ ", "[").replace(" ]", "]")
            # Align `trajectory` with the rest of the keys
            lines[i] = lines[i].split('"trajectory":')[0] + combined.strip()
            del lines[i + 1:j + 1]  # Remove the now redundant lines
    return "\n".join(lines)


def main():
    # Number of people to generate
    n_of_people = 15

    # Possible values for gender
    _gender = ["male", "female"]

    # Possible values for hat and bag
    _bool = ["true", "false"]

    # Output dictionary
    output_dict = {"people": []}

    # Output file path
    output_filename = "../output.json"

    # Generate data for each person
    for i in range(1, n_of_people + 1):
        length = random.randint(1, 5)
        person = {
            "id": i,
            "gender": random.choice(_gender),
            "bag": random.choice(_bool),
            "hat": random.choice(_bool),
            "trajectory": [random.randint(1, 4) for _ in range(length)],
        }
        output_dict["people"].append(person)

    # Write the formatted JSON to the output file
    with open(output_filename, "w") as fp:
        fp.write(custom_dumps(output_dict))


if __name__ == '__main__':
    main()
