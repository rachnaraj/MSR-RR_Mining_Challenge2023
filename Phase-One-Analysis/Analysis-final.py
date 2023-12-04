import json
import os
import re

def analyse_json_file(relevant_data, keyword, output_file_path):
    print(f"Total size of relevant_data: {len(relevant_data)}")

    # Count occurrences of 'ListOfCode' types
    code_types_count = {'java': 0, 'javascript': 0, 'python': 0}
    for conversation in relevant_data:
        if isinstance(conversation, dict) and 'ListOfCode' in conversation:
            for code_block in conversation['ListOfCode']:
                if isinstance(code_block, dict) and 'Type' in code_block:
                    code_type = code_block['Type']
                    if code_type in code_types_count:
                        code_types_count[code_type] += 1

    print(f"Count of ListOfCode types:")
    for code_type, count in code_types_count.items():
        print(f"{code_type}: {count}")

    # Save the outputs into a file in the same location
    output_data = {
        "Type": keyword,
        "TotalSize": len(relevant_data),
        "CodeTypesCount": code_types_count
    }

    # Check if the file exists
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            data[keyword] = output_data

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, indent=2)
    else:
        data[keyword] = output_data
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, indent=2)

    print(f"Outputs saved to: {output_file_path}")

if __name__ == "__main__":
    folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\New-Dataset\DevGPT\Extracted-dataset'
    output_file_path = os.path.join(folder_path, "Analysis.json")

    # List all files in the folder
    file_list = os.listdir(folder_path)

    # Filter only JSON files
    json_files = [f for f in file_list if f.endswith('.json')]

    # Access JSON files one by one
    file_pattern = re.compile(r'\d{8}_\d{6}_(\w+)_sharings')

    for json_file in json_files:
        match = file_pattern.match(json_file)
        if match:
            keyword = match.group(1)

        # Construct the full path to the JSON file
        full_path = os.path.join(folder_path, json_file)

        with open(full_path, 'r') as f:
            relevant_data = json.load(f)

        analyse_json_file(relevant_data, keyword, output_file_path)
