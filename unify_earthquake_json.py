import json
import os
import glob
from pathlib import Path

# Define input and output directories
# Adjust these paths if your directories are different
DETAILED_STATION_JSON_DIR = Path("earthquake_data/json_with_city")
REGIONAL_INTENSITY_JSON_DIR = Path("earthquake_regional_data")
UNIFIED_JSON_DIR = Path("unified_earthquake_data")

# Ensure the output directory exists
UNIFIED_JSON_DIR.mkdir(parents=True, exist_ok=True)

def transform_detailed_station_data(data, event_id):
    unified = {
        "event_id": event_id,
        "timestamp": data.get("timestamp"),
        "epicenter_latitude": data.get("latitude"),
        "epicenter_longitude": data.get("longitude"),
        "depth_km": data.get("depth_km"),
        "magnitude": data.get("magnitude"),
        "max_intensity_observed": None, # Will calculate from stations
        "source_type": "detailed_station",
        "affected_locations": []
    }

    max_int = 0
    for station in data.get("stations", []):
        intensity = station.get("Int")
        if isinstance(intensity, (int, float)): # Check if intensity is a number
             max_int = max(max_int, int(intensity))

        location = {
            "location_name": station.get("Staname"),
            "latitude": station.get("Stalat"),
            "longitude": station.get("Stalon"),
            "county": station.get("City"), # Assuming 'City' was added previously
            "intensity": intensity,
            "station_code": station.get("Stacode"),
            "distance_km": station.get("Dist"),
            "pga_v": station.get("PGA(V)"),
            "pga_ns": station.get("PGA(NS)"),
            "pga_ew": station.get("PGA(EW)"),
            "pgv_v": station.get("PGV(V)"),
            "pgv_ns": station.get("PGV(NS)"),
            "pgv_ew": station.get("PGV(EW)")
        }
        unified["affected_locations"].append(location)

    unified["max_intensity_observed"] = max_int if max_int > 0 else None
    return unified

def transform_regional_intensity_data(data, event_id):
    # Attempt to parse timestamp from event_id (assuming format YYYYMMDDHHMMSS...)
    timestamp_str = None
    try:
        # Extract the numeric part assuming it's at the beginning
        numeric_part = "".join(filter(str.isdigit, event_id.split('_')[0]))
        if len(numeric_part) >= 14: # Need at least YYYYMMDDHHMMSS
            year = numeric_part[0:4]
            month = numeric_part[4:6]
            day = numeric_part[6:8]
            hour = numeric_part[8:10]
            minute = numeric_part[10:12]
            second = numeric_part[12:14]
            timestamp_str = f"{year}-{month}-{day} {hour}:{minute}:{second}"
    except Exception:
        timestamp_str = None # Keep it None if parsing fails

    unified = {
        "event_id": event_id,
        "timestamp": timestamp_str, # Use parsed timestamp
        "epicenter_latitude": data.get("epicenter_lat"),
        "epicenter_longitude": data.get("epicenter_lon"),
        "depth_km": None, # Not available in this source
        "magnitude": data.get("magnitude"),
        "max_intensity_observed": data.get("max_intensity"),
        "source_type": "regional_intensity",
        "affected_locations": []
    }

    for loc in data.get("locations", []):
        location = {
            "location_name": loc.get("location_name"),
            "latitude": loc.get("latitude"),
            "longitude": loc.get("longitude"),
            "county": loc.get("county"),
            "intensity": loc.get("intensity"),
            # Fields below are not available in regional data
            "station_code": None,
            "distance_km": None,
            "pga_v": None,
            "pga_ns": None,
            "pga_ew": None,
            "pgv_v": None,
            "pgv_ns": None,
            "pgv_ew": None
        }
        unified["affected_locations"].append(location)

    return unified

def process_json_file(filepath, output_dir):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        event_id = filepath.stem # Get filename without extension (e.g., "2014_001")
        unified_data = None

        # Detect format and transform
        if "stations" in data and isinstance(data["stations"], list):
            unified_data = transform_detailed_station_data(data, event_id)
            print(f"Processed (detailed): {filepath.name}")
        elif "locations" in data and isinstance(data["locations"], list):
            unified_data = transform_regional_intensity_data(data, event_id)
            print(f"Processed (regional): {filepath.name}")
        else:
            print(f"Skipping unknown format: {filepath.name}")
            return

        # Save the unified data
        output_filepath = output_dir / f"{event_id}.json"
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(unified_data, f, ensure_ascii=False, indent=4)

    except json.JSONDecodeError:
        print(f"Error decoding JSON: {filepath.name}")
    except Exception as e:
        print(f"Error processing file {filepath.name}: {e}")

# Process files from both directories
for filepath in DETAILED_STATION_JSON_DIR.glob("*.json"):
    process_json_file(filepath, UNIFIED_JSON_DIR)

for filepath in REGIONAL_INTENSITY_JSON_DIR.glob("*.json"):
    process_json_file(filepath, UNIFIED_JSON_DIR)



print(f"\\nUnified JSON files saved to: {UNIFIED_JSON_DIR}")