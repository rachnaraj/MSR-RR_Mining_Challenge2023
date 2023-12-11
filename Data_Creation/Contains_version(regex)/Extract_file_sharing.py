import json
import re
import os

def capture_version(input_text):
    pattern = r'\^?\d+\.\d+\.\d+\b'
    # pattern = r'"(\d+\.\d+\.\d+(?:[^"]*\\)?)\"'  # For versions within double quotes
    match = re.search(pattern, input_text)
    
    if match:
        print(match)
        return match.group(0)
    else:
        return False
    
    


def extract_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    relevant_data = []
    
    for entry in data:
        version_match = []
        conversations = entry.get('Conversation', [])
        found = False
        for conversation in conversations:
            # print("entering!!!")
            prompt = conversation.get('Prompt', '')
            answer = conversation.get('Answer', '')
            list_of_code = conversation.get('ListOfCode', [])
            
            if ((capture_version(answer) or capture_version(prompt))):
                version_obtained = capture_version(answer)
                version_obtained_1 = capture_version(prompt)
                if version_obtained:
                    found= True
                    version_match.append(version_obtained)
                elif version_obtained_1:
                    found= True
                    version_match.append(version_obtained_1)
                print(version_match)
                
                
               
        if found:
            relevant_data.append({
                'Contains_version': True,
                'version_found':version_match,
                'content': entry

            })


                    
            # print(relevant_data)
    return relevant_data





def save_to_json(data, output_folder, filename):
    output_file_path = os.path.join(output_folder, f"{filename}.json")
    with open(output_file_path, 'w', encoding='utf-8') as output_json:
        json.dump(data, output_json, indent=2)
    print(f"Data saved to {output_file_path}")

def process_files(output_folder):
    file_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contain_lib_code_import_2\file_sharings.json'

    relevant_data = extract_info(file_path)
    if relevant_data:
        save_to_json(relevant_data, output_folder, 'file_sharings')
        print(len(relevant_data))
    else:
        print("No relevant data found!")
    print(f"All files processed.")

if __name__ == "__main__":
    output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contains_version(regex)'  # Replace with the desired output folder
    process_files(output_folder_path)
