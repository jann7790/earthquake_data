import json
import os
import glob

# Define the allowed counties
allowed_counties = {"臺北市", "臺中市", "臺南市", "新竹市"}

# Path to the earthquake data directory
earthquake_data_dir = "/home/user/tsmc/earthquake_regional_data"

# Process all JSON files in the directory
for json_file_path in glob.glob(os.path.join(earthquake_data_dir, "*.json")):
    print(f"Processing {json_file_path}")
    
    # Read the JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter the locations
    original_count = len(data['locations'])
    data['locations'] = [loc for loc in data['locations'] if loc['county'] in allowed_counties]
    filtered_count = len(data['locations'])
    
    # Write back the filtered data
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Filtered {original_count - filtered_count} locations, kept {filtered_count} locations")

print("Processing complete!")
