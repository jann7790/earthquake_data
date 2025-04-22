import csv
import os
import sys
import subprocess
import re
from datetime import datetime
import requests
import json

def encode_row(row):
    """
    Encodes a single earthquake data row based on specific columns.
    
    Args:
        row: A list containing earthquake data columns.
        
    Returns:
        tuple: (encoded_string, error_message)
            - encoded_string: The encoded string if successful, None otherwise.
            - error_message: Error message if encoding fails, None otherwise.
    """
    # Ensure row has enough columns
    if len(row) < 8:
        return None, f"Insufficient columns ({len(row)})"
    
    earthquake_id_raw = row[0]
    time_raw = row[1]
    magnitude_raw = row[4]
    
    # Clean data
    earthquake_id = earthquake_id_raw.strip()
    
    # Skip row if earthquake_id is not numeric

    
    cleaned_time = time_raw.replace('-', '').replace(' ', '').replace(':', '')
    cleaned_magnitude = magnitude_raw.replace('.', '')
    if len(cleaned_magnitude) == 1:
        cleaned_magnitude = cleaned_magnitude + '0'
    
    # Validate cleaned time and magnitude look reasonable (simple check)
    if not cleaned_time.isdigit() or len(cleaned_time) != 14:
        return None, f"Invalid time format '{time_raw}'"
    if not cleaned_magnitude.isdigit():
        return None, f"Invalid magnitude format '{magnitude_raw}'"
    
    # Concatenate according to the specified logic
    if not earthquake_id.isdigit():
        encoded_string = f"{cleaned_time}{cleaned_magnitude}"
    else:
        encoded_string = f"{cleaned_time}{cleaned_magnitude}{earthquake_id}"
    return encoded_string, None


def download_regional_data(url):
    encoded_id = url.split('/')[-1]
    output_dir = './earthquake_regional_data'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{encoded_id}_regional.json")
    if os.path.exists(output_file):
        print(f"File already exists: {output_file}. Skipping download.", file=sys.stderr)
        return None
    """
    Downloads and parses regional earthquake data from CWA website.
    
    Args:
        url: URL of the earthquake details page
        
    Returns:
        list: List of dictionaries containing location data
    """
    try:
        print(f"Downloading regional data from: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to download regional data. Status code: {response.status_code}", file=sys.stderr)
            return None
        
        # Extract locationList from the HTML response
        html_content = response.text
        
        # Find the locationList JavaScript array
        match = re.search(r'var locationList = \[(.*?)\];', html_content, re.DOTALL)
        if not match:
            print("Could not find locationList in the HTML content", file=sys.stderr)
            return None
            
        location_list_str = match.group(1)
        
        # Parse the JavaScript array into a Python list
        locations = []
        for loc_match in re.finditer(r'\[\'(.*?)\', \'(.*?)\', \'(.*?)\', \'(.*?)\', \'(.*?)\'\]', location_list_str):
            lat, lon, county, intensity, location_name = loc_match.groups()
            locations.append({
                'latitude': lat,
                'longitude': lon,
                'county': county,
                'intensity': intensity,
                'location_name': location_name
            })
        
        # Extract earthquake basic information
        lat_match = re.search(r'var lat = \'(.*?)\';', html_content)
        lon_match = re.search(r'var lon = \'(.*?)\';', html_content)
        mag_match = re.search(r'var mag = \'(.*?)\';', html_content)
        max_intensity_match = re.search(r'var maxIntensity = \'(.*?)\';', html_content)
        
        earthquake_info = {
            'epicenter_lat': lat_match.group(1) if lat_match else '',
            'epicenter_lon': lon_match.group(1) if lon_match else '',
            'magnitude': mag_match.group(1) if mag_match else '',
            'max_intensity': max_intensity_match.group(1) if max_intensity_match else '',
            'locations': locations
        }
        
        # Extract the encoded ID to use in the filename

        
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(earthquake_info, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully saved regional data to: {output_file}")
        print(f"Found {len(locations)} affected locations")
        
        return earthquake_info
        
    except Exception as e:
        print(f"Error processing regional data: {e}", file=sys.stderr)
        return None

def download_earthquake_data(csv_filepath, output_dir):
    """
    Reads an earthquake CSV file and downloads related data files from the CWA website.
    
    URL format: https://scweb.cwa.gov.tw/zh-tw/earthquake/download?file=%2FdrawTrace%2Foutcome%2F{year}%2F{year}{編號}.txt
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(csv_filepath, 'r', encoding='big5') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip header row
            
            print(f"Processing CSV file: {csv_filepath}")
            print(f"Downloading files to: {output_dir}")
            print("-" * 40)
            
            for i, row in enumerate(reader):
                try:
                    # Use encode_row to validate and process the row
                    
                    # If encoding was successful, proceed with download
                    earthquake_id_raw = row[0]
                    time_raw = row[1]
                    
                    # Clean earthquake ID (already done in encode_row)
                    earthquake_id = earthquake_id_raw.strip()
                    if not earthquake_id.isdigit():
                        encoded_string, error = encode_row(row)
                        print(encoded_string)
                        url = f"https://scweb.cwa.gov.tw/zh-tw/earthquake/details/{encoded_string}"
                        download_regional_data(url)
                            
                        continue
                        
                    
                    # Extract year from the time field
                    # Assuming time_raw format is like: '2024-04-03 12:34:56'
                    match = re.search(r'(\d{4})-', time_raw)
                    if not match:
                        print(f"Skipping row {i+2}: Cannot extract year from time '{time_raw}'", file=sys.stderr)
                        continue
                    
                    year = match.group(1)

                    # Form the URL
                    url = f"https://scweb.cwa.gov.tw/zh-tw/earthquake/download?file=%2FdrawTrace%2Foutcome%2F{year}%2F{year}{earthquake_id}.txt"
                    output_file = os.path.join(output_dir, f"{year}_{earthquake_id}.txt")
                    if os.path.exists(output_file):
                        print(f"File already exists: {output_file}. Skipping download.", file=sys.stderr)
                        continue
                    
                    print(f"Downloading: {url}")
                    print(f"Output file: {output_file}")
                    
                    # Use wget to download the file
                    cmd = ["wget", "-O", output_file, url]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"Successfully downloaded: {output_file}")
                    else:
                        print(f"Failed to download {url}. Error: {result.stderr}", file=sys.stderr)
                    
                    # Add a small delay to avoid overloading the server
                    subprocess.run(["sleep", "1"])
                    
                except Exception as e:
                    print(f"Error processing row {i+2}: {e}", file=sys.stderr)
    
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_filepath}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


from glob import glob
if __name__ == "__main__":
    csvfiles = glob('./*.csv')
    for csvfile in csvfiles:
        print(f"Found CSV file: {csvfile}")
        # Specify where to save the downloaded files
        output_directory = './earthquake_data'
        
        # Run the download function
        download_earthquake_data(csvfile, output_directory)
        
    print("Download process completed.")
