import re
import json
import os

def convert_to_json(raw_data):
    # Initialize an empty dictionary to store the key-value pairs
    data_dict = {}

    # Use regular expression to find all key-value pairs in the raw data
    pattern = re.compile(r'^(.*?):\s*(.*)$', re.MULTILINE)
    matches = pattern.findall(raw_data)

    for match in matches:
        key, value = match
        key = key.lower()
        if key == "accept-encoding":
            value = "gzip, deflate"
        data_dict[key] = value

    # Convert the dictionary to a JSON string with pretty print
    json_data = json.dumps(data_dict, indent=4)
    return json_data

def save_json_file(filename, json_data):
    with open(filename, 'w') as json_file:
        json_file.write(json_data)

def check_file_exists(filename, raw_data=None):
    # Check if the file exists in the current directory
    if os.path.isfile(filename):
        print(f"The file '{filename}' exists in the current folder.")
    else:
        if raw_data is None:
            # Prompt user for raw data input in terminal (for non-GUI usage)
            print("Please enter the RequestHeader raw data from Firefox (press Enter twice to finish):")
            raw_data = ""
            while True:
                line = input()
                if line == "":
                    break
                raw_data += line + "\n"

        # Call the function and print the result
        json_data = convert_to_json(raw_data)

        # Write the JSON data to a file
        output_filename = filename
        save_json_file(output_filename, json_data)
        print(f"{filename} file has been generated")
