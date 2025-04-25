#!/usr/bin/env python3

import json
import sys
import glob
import os
code_to_city = {'HWA': '花蓮市', 'ETL': '花蓮縣', 'EYL': '花蓮縣', 'ETM': '花蓮縣', 'EHP': '花蓮縣', 'ESL': '花蓮縣', 'EAH': '宜蘭縣', 'EGC': '花蓮縣', 'WHF': '南投縣', 'ENA': '宜蘭縣', 'FUSS': '臺中市', 'EWT': '宜蘭縣', 'EGFH': '花蓮縣', 'NNS': '宜蘭縣', 'TWT': '臺中市', 'NDS': '宜蘭縣', 'ENT': '宜蘭縣', 'TWD': '花蓮縣', 'ETLH': '花蓮縣', 'OWD': '南投縣', 'B112': '彰化縣', 'SSD': '屏東縣', 'SPT': '屏東市', 'SGL': '屏東縣', 'ECL': '臺東縣', 'KAU': '高雄市', 'TWG': '臺東縣', 'ECU': '臺東縣', 'SGS': '高雄市', 'CHN3': '臺南市', 'STY': '高雄市', 'TAI': '臺南市', 'CHN1': '內市', 'TAI1': '臺南市', 'WTP': '嘉義縣', 'SSH': '臺南市', 'ELD': '臺東縣', 'EDH': '臺東縣', 'ECS': '臺東縣', 'SCL': '臺南市', 'CHN4': '嘉義縣', 'ALS': '嘉義縣', 'CHY': '嘉義市', 'CHN5': '雲林縣', 'WGK': '雲林縣', 'WSF': '雲林縣', 'WDL': '斗六市', 'WTC': '彰化縣', 'PNG': '馬公市', 'WCH': '彰化市', 'TWL': '臺南市', 'TWC': '宜蘭縣', 'ILA': '宜蘭市', 'NTC': '宜蘭縣', 'TWE': '宜蘭縣', 'TIPB': '新北市', 'TWB1': '新北市', 'NDT': '宜蘭縣', 'NWF': '新北市', 'TWA': '臺北市', 'NHDH': '新北市', 'NSK': '桃園市', 'NHY': '臺北市', 'TAP': '臺北市', 'BAC': '新北市', 'NWR': '新北市', 'TWS1': '新北市', 'NTY': '桃園市', 'NTS': '新北市', 'KSHI': '新竹縣', 'NFF': '新竹縣', 'NCU': '桃園市', 'NJD': '新竹縣', 'LIOB': '新竹縣', 'NST': '苗栗縣', 'HSN1': '新竹市', 'HSN': '竹北市', 'NHW': '桃園市', 'SHUL': '花蓮縣', 'WHP': '臺中市', 'NJN': '苗栗縣', 'NML': '苗栗市', 'NSY': '苗栗縣', 'WCS': '南投縣', 'TWQ1': '苗栗縣', 'WDJ': '臺中市', 'WWC': '台中港市鎮中心', 'WNT1': '南投市', 'WHY': '南投縣', 'WCH2': '彰化市', 'WYL': '員林市', 'YUS': '南投縣', 'WRL': '彰化縣', 'WTK': '雲林縣', 'WCKO': '嘉義縣', 'CHN2': '嘉義縣', 'WML': '雲林縣', 'CHY1': '朴子市', 'EGA': '花蓮縣', 'NLD': '宜蘭縣', 'ESF': '花蓮縣', 'NOU': '基隆市', 'EHY': '花蓮縣', 'ECB': '臺東縣', 'FULB': '花蓮縣', 'TCU': '臺中市', 'CHK': '臺東縣', 'WCHH': '彰化市', 'NXZ': '新北市', 'WSL': '雲林縣', 'TTN': '臺東市', 'LDU': '臺東縣', 'TWF1': '花蓮縣', 'TAW': '臺東縣', 'EAS': '臺東縣', 'SCZ': '屏東縣', 'LAY': '臺東縣', 'TWM1': '高雄市', 'EGF': '花蓮縣', 'HEN': '屏東縣', 'SNW': '屏東縣', 'WLC': '屏東縣', 'SEB': '屏東縣', 'SML': '南投縣', 'TYC': '南投縣', 'SCK': '臺南市', 'WES': '彰化縣', 'CHN7': '嘉義縣', 'WNT': '南投縣', 'WPL': '南投縣', 'WWF': '臺中市', 'WDD': '臺中市', 'WDS': '臺中市', 'WYP': '臺中市', 'NSD': '苗栗縣', 'EYUL': '花蓮縣', 'C015': '臺南市', 'CHN8': '嘉義縣', 'LONT': '臺東縣', 'SMG': '屏東縣', 'STYH': '高雄市立桃源國民中學', 'SNS': '臺南市', 'SHH': '臺南市', 'SLG': '高雄市', 'SCS': '高雄市', 'EGS': '宜蘭縣', 'NWL': '新北市', 'A124': '新北市', 'B011': '桃園市', 'NSX': '新北市', 'B219': '臺中市', 'A024': '新北市', 'WJS': '南投縣', 'C092': '雲林縣', 'EHD': '臺東縣', 'WCH1': '彰化市', 'NMLH': '苗栗市', 'SNJ': '高雄市', 'D009': '高雄市', 'WSS': '高雄市', 'KAU1': '高雄市', 'SSP': '屏東縣', 'WDG': '澎湖縣', 'TAWH': '臺東縣', 'SLIU': '屏東縣', 'SMS': '屏東縣', 'WDLH': '斗六市', 'NPL': '新北市', 'NHD': '新北市', 'NGL': '新北市', 'ANP': '臺北市', 'NSM': '新北市', 'ESA': '宜蘭縣', 'TWK1': '屏東縣', 'ICHU': '嘉義縣', 'D033': '屏東縣', 'PCY': '基隆市', 'KNM': '金門縣', 'MSU': '連江縣', 'H176': '苗栗縣', 'CHKH': '臺東縣', 'EHYH': '花蓮縣', 'WLCH': '屏東縣', 'DPDB': '南投縣'}

def add_city_to_earthquake_data(earthquake_data):
    """Add city information to each station in the earthquake data based on station code."""
    valid_cities = {"臺北市", "臺中市", "臺南市", "新竹市"}
    filtered_stations = []
    
    for station in earthquake_data.get("stations", []):
        if "Stacode" in station:
            station_code = station["Stacode"]
            
            if station_code in code_to_city:
                city = code_to_city[station_code]
                if city in valid_cities:
                    station["City"] = city
                    filtered_stations.append(station)
            else:
                station["City"] = "Unknown"
    
    earthquake_data["stations"] = filtered_stations
    return earthquake_data

def process_file(input_file, output_file=None):
    """Process a single JSON file to add city information."""
    try:
        with open(input_file, 'r') as f:
            earthquake_data = json.load(f)
        
        updated_data = add_city_to_earthquake_data(earthquake_data)
        
        if output_file:
            # Write to the output file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(updated_data, ensure_ascii=False, indent=2, fp=f)
            print(f"Updated data written to {output_file}")
        else:
            # Output to stdout if no output file specified
            print(json.dumps(updated_data, ensure_ascii=False, indent=2))
            
        return True
    except Exception as e:
        print(f"Error processing file {input_file}: {e}")
        return False

def main():
    # Hardcoded paths
    input_pattern = "./earthquake_data/json/*.json"
    output_dir = "./earthquake_data/json_with_city"
    
    json_files = glob.glob(input_pattern)
    if not json_files:
        print(f"No files found matching pattern: {input_pattern}")
        return
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    processed = 0
    for json_file in json_files:
        # Create output filename in the output directory
        base_name = os.path.basename(json_file)
        output_file = os.path.join(output_dir, base_name)
        
        if process_file(json_file, output_file):
            processed += 1
    
    print(f"Processed {processed} of {len(json_files)} files")
    print(f"City information added to all stations. Results saved in {output_dir}")

if __name__ == "__main__":
    main()