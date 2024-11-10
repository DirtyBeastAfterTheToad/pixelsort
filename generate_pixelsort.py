import os
import random
import subprocess
import sys
from datetime import datetime

# Define sorting functions
SORTING_FUNCTIONS = ["lightness", "hue", "saturation", "intensity", "minimum"]

# Define interval functions and their associated parameters with types
INTERVAL_FUNCTIONS = {
    "threshold": {
        "params": [
            {"flag": "-t", "type": float, "range": (0.0, 1.0)},  # lower threshold
            {"flag": "-u", "type": float, "range": (0.5, 1.0)}   # upper threshold
        ]
    },
    "random": {
        "params": [
            {"flag": "-c", "type": int, "range": (10, 100)},     # characteristic length
            {"flag": "-r", "type": float, "range": (0.0, 1.0)}   # randomness
        ]
    },
    "waves": {
        "params": [
            {"flag": "-c", "type": int, "range": (10, 100)},     # characteristic length
            {"flag": "-a", "type": float, "range": (0, 360)}     # angle in degrees
        ]
    },
    "edges": {
        "params": [
            {"flag": "-t", "type": float, "range": (0.0, 1.0)}   # lower threshold
        ]
    }
}

PIXELSORT_SCRIPT = "pixelsort"

def generate_images(input_file):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    timestamp = datetime.now().strftime("%Y%m%d")
    output_dir = f"output_images/{base_name}_{timestamp}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for interval, details in INTERVAL_FUNCTIONS.items():
        interval_folder = os.path.join(output_dir, interval)
        if not os.path.exists(interval_folder):
            os.makedirs(interval_folder)

        for _ in range(5):  # Generate 5 variations
            # Prepare parameters for each interval function
            params = []
            for param in details["params"]:
                value = random.uniform(*param["range"]) if param["type"] == float else random.randint(*param["range"])
                params.extend([param["flag"], str(value)])

            # Loop through all sorting functions
            for sorting in SORTING_FUNCTIONS:
                output_file = os.path.join(
                    interval_folder,
                    f"{base_name}_{interval}_{sorting}_{'_'.join(params)}.png"
                )

                # Construct the command to run pixelsort
                command = [
                    "python", PIXELSORT_SCRIPT,
                    input_file,
                    "-o", output_file,
                    "-s", sorting,
                    "-i", interval
                ] + params

                # Run the command
                try:
                    print(f"Running command: {' '.join(command)}")
                    subprocess.run(command, check=True)
                    print(f"Generated: {output_file}")
                except subprocess.CalledProcessError as e:
                    print(f"Error generating {output_file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_pixelsort.py <input_image>")
        sys.exit(1)

    input_image = sys.argv[1]
    if not os.path.isfile(input_image):
        print(f"Error: File '{input_image}' not found.")
        sys.exit(1)

    generate_images(input_image)
    print("Processing complete!")
