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
                    if any(capture_version(match) for match in re.finditer(r'\b\d+\.\d+\.\d+(-\w+(\.\d+)?)?\b', answer)) or any(capture_version(match) for match in re.finditer(r'\b\d+\.\d+\.\d+(-\w+(\.\d+)?)?\b', prompt)) or any(capture_version(match) for match in re.finditer(r'\b\d+\.\d+\.\d+(-\w+(\.\d+)?)?\b', code)):
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
    file_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contain_lib_code_import_2\hn_sharings.json'
   
    relevant_data = extract_info(file_path)
    # print("&&&&&&&&&&&&&&&&&&&&&&&&&&" , relevant_data)
    if relevant_data:
        print(len(relevant_data))
        save_to_json(relevant_data, output_folder, 'hn_sharings')
    else:
        print("No relevant data found!")
    print(f"All files processed.")

if __name__ == "__main__":
    # base_folder = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Phase-four-Implementation'
    output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contains_version_and_download_suggestion' # Replace with the desired output folder
    
    process_files(output_folder_path)
