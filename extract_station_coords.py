# extract_station_coords.py
import os
import json
import glob

def extract_coordinates_from_json(json_dir):
    """
    Reads JSON files from a directory, extracts station coordinates,
    and returns a dictionary mapping Stacode to [Longitude, Latitude].
    """
    station_coordinates = {}
    json_files = glob.glob(os.path.join(json_dir, '*.json'))

    if not json_files:
        print(f"No JSON files found in directory: {json_dir}")
        return station_coordinates

    print(f"Found {len(json_files)} JSON files to process.")

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for station in data.get('stations', []):
                stacode = station.get('Stacode')
                stalon = station.get('Stalon')
                stalat = station.get('Stalat')

                if stacode and stalon is not None and stalat is not None:
                    # Update coordinates, potentially overwriting if a station appears in multiple files
                    # (assuming coordinates are consistent or the latest one is desired)
                    station_coordinates[stacode] = [stalon, stalat]
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}")
        except Exception as e:
            print(f"An error occurred processing file {file_path}: {e}")

    return station_coordinates

if __name__ == "__main__":
    # Directory containing the processed JSON files
    # Assumes the JSON files are in a 'json' subdirectory within 'earthquake_data'
    json_directory = './earthquake_data/json'

    coordinates_dict = extract_coordinates_from_json(json_directory)

    if coordinates_dict:
        print("\nStation Coordinates (Stacode: [Longitude, Latitude]):")
        # Pretty print the dictionary
        print(json.dumps(coordinates_dict, ensure_ascii=False))
    else:
        print("No station coordinates were extracted.")
