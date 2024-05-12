print("Script is starting ...")
import json
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_blood_pressure_from_xml(xml_file):
    # Parse XML with ElementTree
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Create list to hold dictionaries
    dict_list = []

    # Iterate over each child element in root
    for element in root.iter('Record'):
        # Check if element has 'type' attribute and it's one of the desired ones
        if 'type' in element.attrib and element.attrib['type'] in ['HKQuantityTypeIdentifierBloodPressureSystolic', 'HKQuantityTypeIdentifierBloodPressureDiastolic']:
            # Create dictionary to hold data from this element
            data_dict = {}
            # Add type, value, creationDate, startDate, and endDate to dictionary
            data_dict['Type'] = element.attrib['type']
            data_dict['value'] = element.attrib.get('value')
            data_dict['creationDate'] = element.attrib.get('creationDate')
            data_dict['startDate'] = element.attrib.get('startDate')
            data_dict['endDate'] = element.attrib.get('endDate')

            # Append dictionary to list
            dict_list.append(data_dict)

    # Print the number of entries extracted
    print(f"Number of entries extracted: {len(dict_list)}")
    
    # Return list of dictionaries
    return dict_list

def append_to_json(json_file, data):
    # Open the JSON file
    with open(json_file, 'r+') as f:
        # Load existing data
        file_data = json.load(f)

        # Count the number of entries before appending
        count_before = len(file_data)

        # Append new data that is not already in file_data
        file_data.extend([entry for entry in data if not any(existing_entry['Type'] == entry['Type'] and existing_entry['creationDate'] == entry['creationDate'] for existing_entry in file_data)])

        # Count the number of entries after appending
        count_after = len(file_data)

        # Move file pointer to beginning of file
        f.seek(0)

        # Clear the file content
        f.truncate()

        # Print the number of entries appended
        print(f"Number of new entries appended: {count_after - count_before}")

        # Write new data to file
        json.dump(file_data, f)

        
def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S %z')
        return True
    except ValueError:
        return False

APPLE_FILE = 'exported_data/export.xml'
JSON_FILE = 'analytics/blood_pressure_data.json'

new_data = parse_blood_pressure_from_xml(APPLE_FILE)  # remove JSON_FILE from here
append_to_json(JSON_FILE, new_data)
print("Script has completed ...")