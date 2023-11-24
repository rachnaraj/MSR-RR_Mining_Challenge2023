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
                            for code_block in conversation.get('ListOfCode', []):
                                if 'Type' in code_block:
                                    code_type = code_block.get('Type', '')
                                    prompt = conversation.get('Prompt', '')

                                    # Print the prompt for debugging
                                    print("Prompt:", prompt)

                                    # Use regex to check if the prompt contains the word "import"
                                    if re.search(r'\bimport\b', prompt):
                                        # Check if the code_type is in the specified list
                                        if code_type in ['java', 'javascript', 'python', 'typescript']:
                                            relevant_conversations.append({
                                                'FileType': source_type,
                                                'Type': code_type,
                                                'Prompt': prompt,
                                                'Conversations': chatgpt_sharing['Conversations']
                                            })

    return relevant_conversations

def save_to_json(data, output_folder, filename):
    output_file_path = os.path.join(output_folder, f"{filename}_import_output.json")
    with open(output_file_path, 'w', encoding='utf-8') as output_json:
        json.dump(data, output_json, indent=2)
    print(f"Data saved to {output_file_path}")



def process_files(base_folder, output_folder,file_pattern):
    file_paths = [f for f in glob.glob(os.path.join(base_folder, 'snapshot*', '**', file_pattern), recursive=True)]
    # print(f"Processing file: {file_paths}")
    counter  = 0
    for file_path in file_paths:
        # file_name = os.path.splitext(file_path)
        counter 
        # print("First file##################")
        relevant_data = extract_info(file_path)
        # print("&&&&&&&&&&&&&&&&&&&&&&&&&&" , relevant_data)
    if relevant_data:
        save_to_json(relevant_data, output_folder, file_path.split('\\')[-1])

    print(f"All files processed.")

if __name__ == "__main__":
    base_folder = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\New-Dataset\DevGPT'
    output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Phase-three-Implementation'  # Replace with the desired output folder
    file_pattern = '*_hn_sharings.json'
    # Process all JSON files in the input folder and save with different names in the output folder
    process_files(base_folder, output_folder_path, file_pattern)
