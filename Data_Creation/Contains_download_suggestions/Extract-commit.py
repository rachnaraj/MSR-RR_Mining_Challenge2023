import json
import re
import os

def is_semantic_version(version_string):
    return re.match(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$', version_string.group()) is not None

def contains_install_keywords(text):
    install_keywords = ["pip install", "conda install", "npm install", "mvn install"]
    return any(keyword in text for keyword in install_keywords)


def extract_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    relevant_data = []
    
    for entry in data:
        conversations = entry.get('Conversation', [])
        
        for conversation in conversations:
            # print("entering!!!")
            prompt = conversation.get('Prompt', '')
            answer = conversation.get('Answer', '')
            list_of_code = conversation.get('ListOfCode', [])
            for content in list_of_code:
                code = content.get('Content', '')
                if (contains_install_keywords(answer) or contains_install_keywords(code)):
                    relevant_data.append({
                        'content': entry
                    })
                    break
            break

                    
            # print(relevant_data)
    return relevant_data



def save_to_json(data, output_folder, filename):
    output_file_path = os.path.join(output_folder, f"{filename}.json")
    with open(output_file_path, 'w', encoding='utf-8') as output_json:
        json.dump(data, output_json, indent=2)
    print(f"Data saved to {output_file_path}")

def process_files(output_folder):
    file_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contains_library_code_import\commit_sharings_.json'
   
    relevant_data = extract_info(file_path)
    # print("&&&&&&&&&&&&&&&&&&&&&&&&&&" , relevant_data)
    if relevant_data:
        print(len(relevant_data))
        save_to_json(relevant_data, output_folder, 'commit_sharings')
    else:
        print("No relevant data found!")
    print(f"All files processed.")

if __name__ == "__main__":
    # base_folder = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Phase-four-Implementation'
    output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contains_download_suggestions' # Replace with the desired output folder
    
    process_files(output_folder_path)
