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

    relevant_data = []
    
    for entry in data:
        conversations = entry.get('Conversations', [])
        
        for conversation in conversations:
            prompt = conversation.get('Prompt', '')
            answer = conversation.get('Answer', '')
            list_of_code = conversation.get('ListOfCode', [])
            
            for content in list_of_code:
                code = content.get('Content', '')
                
                if (contains_install_keywords(answer) or contains_install_keywords(code)) and \
                   any(is_semantic_version(match) for match in re.finditer(r'\b\d+\.\d+\.\d+(-\w+(\.\d+)?)?\b', code)):
                    relevant_data.append({
                        'FileType': entry.get('FileType'),
                        'Conversations': conversations,
                    })
            

    return relevant_data



def save_to_json(data, output_folder, filename):
    output_file_path = os.path.join(output_folder, f"{filename}_version_output.json")
    with open(output_file_path, 'w', encoding='utf-8') as output_json:
        json.dump(data, output_json, indent=2)
    print(f"Data saved to {output_file_path}")



def process_files(output_folder):
    file_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Phase-four-2-Implementation\20230831_063412_commit_sharings.json_import_output.json'
   
    relevant_data = extract_info(file_path)
    # print("&&&&&&&&&&&&&&&&&&&&&&&&&&" , relevant_data)
    if relevant_data:
        print(len(relevant_data))
        save_to_json(relevant_data, output_folder, '20230831_061926_commit_sharings')
    else:
        print("No relevant data found!")
    print(f"All files processed.")

if __name__ == "__main__":
    # base_folder = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Phase-four-Implementation'
    output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Phase-seven-download-sugg-with-version'  # Replace with the desired output folder
    
    process_files(output_folder_path)
