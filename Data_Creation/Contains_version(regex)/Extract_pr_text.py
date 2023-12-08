import json
import re
import os

def is_semantic_version(version_string):
    return re.match(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$', version_string.group()) is not None



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
             
            if re.search(r'\bversion\b',answer):
                # print("yes!!")
                if any(is_semantic_version(match) for match in re.finditer(r'\b\d+\.\d+\.\d+(-\w+(\.\d+)?)?\b', answer)) or any(is_semantic_version(match) for match in re.finditer(r'\b\d+\.\d+\.\d+(-\w+(\.\d+)?)?\b', prompt)):
                    relevant_data.append({
                        'Contains_version': True,
                        'content': entry
                    })
                    break
                else:
                    break

                    
            # print(relevant_data)
    return relevant_data



def save_to_json(data, output_folder, filename):
    output_file_path = os.path.join(output_folder, f"{filename}.json")
    with open(output_file_path, 'w', encoding='utf-8') as output_json:
        json.dump(data, output_json, indent=2)
    print(f"Data saved to {output_file_path}")

def process_files(output_folder):
    file_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contains_library_code_import\pr_sharings.json'
   
    relevant_data = extract_info(file_path)
    # print("&&&&&&&&&&&&&&&&&&&&&&&&&&" , relevant_data)
    if relevant_data:
        print(len(relevant_data))
        save_to_json(relevant_data, output_folder, 'pr_sharings')
    else:
        print("No relevant data found!")
    print(f"All files processed.")

if __name__ == "__main__":
    # base_folder = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Phase-four-Implementation'
    output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contains_version(regex)'  # Replace with the desired output folder
    
    process_files(output_folder_path)
