import os
import json
import re
import glob
from datetime import datetime

def parse_earthquake_file(filepath):
    """
    Parse earthquake data text file into a structured JSON format
    """
    try:
        # Open file with Big5 encoding instead of UTF-8
        with open(filepath, 'r', encoding='big5', errors='replace') as file:
            lines = file.readlines()
        
        if len(lines) < 6:  # At least header info should be present
            print(f"File {filepath} seems incomplete. Skipping.")
            return None
        
        # Extract filename to get earthquake ID
        filename = os.path.basename(filepath)
        earthquake_id = filename.split('_')[1].split('.')[0] if '_' in filename else None
        
        # Parse header information
        header_data = {}
        for i in range(5):  # First 5 lines are header
            if ':' in lines[i]:
                key, value = lines[i].split(':', 1)
                header_data[key.strip()] = value.strip()
        
        # Extract coordinates and clean values
        lat_match = re.search(r'(\d+\.\d+)', header_data.get('Lat', '0'))
        lon_match = re.search(r'(\d+\.\d+)', header_data.get('Lon', '0'))
        
        # Parse timestamp
        timestamp = None
        if 'Origin Time' in header_data:
            try:
                time_str = header_data['Origin Time']
                timestamp = datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S').isoformat()
            except ValueError:
                print(f"Could not parse timestamp: {header_data.get('Origin Time')}")
        
        # Create result object with metadata
        result = {
            "earthquake_id": earthquake_id,
            "timestamp": timestamp,
            "latitude": float(lat_match.group(1)) if lat_match else None,
            "longitude": float(lon_match.group(1)) if lon_match else None,
            "depth_km": float(header_data.get('Depth', '0').replace('km', '')) if 'Depth' in header_data else None,
            "magnitude": float(header_data.get('Mag', '0')) if 'Mag' in header_data else None,
            "stations": []
        }
        
        # Parse station data (lines after header)
        for i in range(5, len(lines)):
            line = lines[i].strip()
            if not line or not line.startswith('Stacode='):
                continue
                
            # Split the line by comma
            parts = line.split(',')
            station = {}
            
            for part in parts:
                if '=' in part:
                    key, value = part.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Convert numeric values to float
                    if re.match(r'^[-+]?\d+\.\d+$', value):
                        value = float(value)
                    elif value.isdigit():
                        value = int(value)
                        
                    station[key] = value
            
            result["stations"].append(station)
            
        return result
        
    except Exception as e:
        print(f"Error parsing {filepath}: {str(e)}")
        return None

def process_earthquake_files(input_dir, output_dir=None):
    """
    Process all earthquake data files in the input directory and 
    save JSON results to the output directory
    """
    if output_dir is None:
        output_dir = os.path.join(input_dir, 'json')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all .txt files in the directory
    file_paths = glob.glob(os.path.join(input_dir, '*.txt'))
    
    for file_path in file_paths:
        print(f"Processing {file_path}...")
        data = parse_earthquake_file(file_path)
        
        if data:
            # Create output filename
            filename = os.path.basename(file_path)
            output_filename = os.path.splitext(filename)[0] + '.json'
            output_path = os.path.join(output_dir, output_filename)
            
            # Write to JSON file with ensure_ascii=False to preserve Chinese characters
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=2, ensure_ascii=False)
            
            print(f"Created {output_path}")
        else:
            print(f"Skipped {file_path} due to parsing errors")

if __name__ == "__main__":
    # Directory containing earthquake data files
    input_directory = './earthquake_data'
    
    # Directory for JSON output (will be created if it doesn't exist)
    output_directory = './earthquake_data/json'
    
    process_earthquake_files(input_directory, output_directory)
    
    # Alternatively, parse a single file:
    # sample_file = '/home/user/tsmc/earthquake_data/2020_009.txt'
    # result = parse_earthquake_file(sample_file)
    # print(json.dumps(result, indent=2, ensure_ascii=False))
