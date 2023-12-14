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
                                    code_content = code_block.get('Content')
                                    # Use regex to check if the prompt contains the word "import"
                                    if (re.search(r'\bimport\b', code_content)) :
                                        # Check if the code_type is in the specified list
                                        if code_type in ['java', 'javascript', 'python', 'typescript']:
                                            relevant_conversations.append({
                                                'FileType': source_type,
                                                'Type': code_type,
                                                'Conversations': chatgpt_sharing['Conversations']
                                            })
        print(len(relevant_conversations))
    return relevant_conversations

def process_files(base_folder,file_pattern):
    file_paths = [f for f in glob.glob(os.path.join(base_folder, 'snapshot*', '**', file_pattern), recursive=True)]
    print(f"Processing file: {file_paths}")
    counter  = 0
    for file_path in file_paths:

        relevant_data = extract_info(file_path)
       
        if relevant_data:
            counter +=len(relevant_data)
            # print(counter)

    print(f"All files processed, count : ", counter)

if __name__ == "__main__":
    base_folder = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\New-Dataset\DevGPT'
    file_pattern = '*_file_sharings.json'
    # Process all JSON files in the input folder and save with different names in the output folder
    process_files(base_folder, file_pattern)
