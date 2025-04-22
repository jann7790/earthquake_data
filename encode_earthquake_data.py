import csv
import sys

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
    if not earthquake_id.isdigit():
        return None, f"Non-numeric ID '{earthquake_id_raw.strip()}'"
    
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
    encoded_string = f"{cleaned_time}{cleaned_magnitude}{earthquake_id}"
    return encoded_string, None

def encode_earthquake_data(filepath):
    """
    Reads an earthquake CSV file, encodes each valid row based on specific columns,
    and prints the encoded string.

    Encoding logic: {cleaned_地震時間}{cleaned_規模}{cleaned_編號}
    - cleaned_地震時間: '地震時間' with '-', ' ', ':' removed.
    - cleaned_規模: '規模' with '.' removed.
    - cleaned_編號: '編號' with leading/trailing whitespace removed.

    Rows are skipped if '編號' is not numeric after cleaning.
    """
    try:
        with open(filepath, 'r', encoding='big5') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader) # Skip header row

            print(f"Processing file: {filepath}")
            print(f"Header: {','.join(header)}")
            print("-" * 20)

            for i, row in enumerate(reader):
                try:
                    encoded_string, error = encode_row(row)
                    if error:
                        print(f"Skipping row {i+2}: {error}", file=sys.stderr)
                        continue
                    
                    print(encoded_string)

                except Exception as e:
                    print(f"Error processing row {i+2}: {row} - {e}", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

# Specify the path to your CSV file
csv_filepath = '/home/user/tsmc/地震活動彙整_638809439021965548.csv'

# Run the encoding function
encode_earthquake_data(csv_filepath)
