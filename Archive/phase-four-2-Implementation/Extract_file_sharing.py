import json
import os
import glob
import re

def extract_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        relevant_conversations = []
        for source in data.get('Sources', []):
            source_type = source.get('Type', '')
            for chatgpt_sharing in source.get('ChatgptSharing', []):
                if chatgpt_sharing.get('Conversations'):
                    for conversation in chatgpt_sharing['Conversations']:
                        if conversation.get('ListOfCode') != []:
                            # Check if any code block in the conversation meets the condition
                            if any(
                                'Type' in code_block and
                                re.search(r'\bimport\b', code_block.get('Content', '')) and
                                code_block['Type'] in ['java', 'javascript', 'python', 'typescript']
                                for code_block in conversation.get('ListOfCode', [])
                            ):
                                relevant_conversations.append({
                                    'FileType': source_type,
                                    'Conversations': chatgpt_sharing['Conversations']
                                })
                                break  # Stop checking other conversations in the same chatgpt_sharing
    return relevant_conversations

def save_to_json(data, output_folder, filename):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the output folder if it doesn't exist

    output_file_name = f"{filename}_import_output.json"
    output_file_path = os.path.join(output_folder, output_file_name)

    with open(output_file_path, 'w', encoding='utf-8') as output_json:
        json.dump(data, output_json, indent=2)
    
    print(f"Data saved to {output_file_path}")

# ...

def process_files(base_folder, output_folder, file_pattern):
    gather_data = []  # Keep this as a flat list

    file_paths = [f for f in glob.glob(os.path.join(base_folder, 'snapshot*', '**', file_pattern), recursive=True)]

    for file_path in file_paths:
        relevant_data = extract_info(file_path)
        print(len(relevant_data))
        if relevant_data:
            gather_data.extend(relevant_data)  # Extend the flat list with conversations from each file
        output_folder_name = file_path.split('\\')[-1]
    if gather_data:
        print(len(gather_data))
        output_folder_name = output_folder_name
        save_to_json(gather_data, output_folder, output_folder_name)
        print(f"All files processed.")
    else:
        print("No relevant data found.")


if __name__ == "__main__":
    base_folder = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\New-Dataset\DevGPT'
    output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\phase-four-2-Implementation'  # Replace with the desired output folder
    file_pattern = '*_file_sharings.json'
    # Process all JSON files in the input folder and save with different names in the output folder
    process_files(base_folder, output_folder_path, file_pattern)
