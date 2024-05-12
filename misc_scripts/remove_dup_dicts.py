print("Script is starting ...")
import pandas as pd

FILE_PATH = 'blood_pressure_data.json'

def remove_duplicates_from_json(input_json_file: str, output_json_file: str) -> None:
    df = pd.read_json(input_json_file)
    
    df = df.drop_duplicates()
    
    df = df.to_json(output_json_file, orient='records')

remove_duplicates_from_json(FILE_PATH, 'no_dups.json')
print("Script has completed ...")
