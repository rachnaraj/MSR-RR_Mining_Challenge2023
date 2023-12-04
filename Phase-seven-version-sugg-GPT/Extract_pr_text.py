import json
import re
import os

def is_semantic_version(version_string):
    return re.match(r'\b(?<!\d\.)\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+(?:\.\d+)?)?(?:\+[a-zA-Z0-9]+(?:\.\d+)?)?\b(?![\d.])', version_string.group()) is not None

def contains_install_keywords(text):
    install_keywords = ["pip install", "conda install", "npm install", "mvn install"]
    return any(keyword in text for keyword in install_keywords)

def extract_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    relevant_data = []  # Use a list to store relevant conversations

    for entry in data:
        conversations = entry.get('Conversations', [])
        relevant_conversations = []

        for conversation in conversations:
            prompt = conversation.get('Prompt', '')
            answer = conversation.get('Answer', '')
            list_of_code = conversation.get('ListOfCode', [])

            # Flag to track if a relevant code has been found in the conversation
            relevant_code_found = False

            # Check if any conversation satisfies the condition
            if (
                (
                    not any(
                        is_semantic_version(match) 
                        for match in re.finditer(r'\b\d+\.\d+\.\d+(-\w+(\.\d+)?)?\b', prompt)
                    )
                ) and (
                    any(
                        is_semantic_version(match) 
                        for match in re.finditer(r'\b\d+\.\d+\.\d+(-\w+(\.\d+)?)?\b', answer)
                    ) or contains_install_keywords(answer) or any(
                        is_semantic_version(match)
                        for code_content in list_of_code
                        for match in re.finditer(r'\b\d+\.\d+\.\d+(-\w+(\.\d+)?)?\b', code_content.get('Content', ''))
                    )
                )
            ):
                relevant_code_found = True
                relevant_conversations.append(conversation)
                break  # Break the loop if a relevant code is found in the conversation

        if relevant_code_found:
            relevant_data.append({
                'FileType': entry.get('FileType'),
                'Conversations': relevant_conversations,
            })

    return relevant_data

def save_to_json(data, output_folder, filename):
    output_file_path = os.path.join(output_folder, f"{filename}_version_output.json")
    with open(output_file_path, 'w', encoding='utf-8') as output_json:
        json.dump(data, output_json, indent=2)
    print(f"Data saved to {output_file_path}")

def process_files(output_folder):
    file_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Phase-four-2-Implementation\20230831_060603_pr_sharings.json_import_output.json'
   
    relevant_data = extract_info(file_path)
    
    if relevant_data:
        print(len(relevant_data))
        save_to_json(relevant_data, output_folder, '20230831_061926_pr_sharings')
    else:
        print("No relevant data found!")
    
    print(f"All files processed.")

if __name__ == "__main__":
    output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Phase-seven-version-sugg-GPT'
    
    process_files(output_folder_path)
