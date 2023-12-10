import json
import re
import os

def capture_version(input_text):
    pattern = r'"(\d+\.\d+\.\d+(?:[^"]*\\)?)\"'  # For versions within double quotes
    match = re.search(pattern, input_text)
    
    if match:
        return match.group(1)
    
    # Additional cases for semantic versions in Java, Python, and JavaScript
    java_pattern = r'\bversion\s*=\s*["\'](\d+\.\d+\.\d+)["\']'  # Java
    python_pattern = r'\bversion\s*=\s*["\'](\d+\.\d+\.\d+)["\']'  # Python
    js_pattern = r'\bversion\s*:\s*["\'](\d+\.\d+\.\d+)["\']'  # JavaScript

    java_match = re.search(java_pattern, input_text, re.IGNORECASE)
    python_match = re.search(python_pattern, input_text, re.IGNORECASE)
    js_match = re.search(js_pattern, input_text, re.IGNORECASE)

    if java_match:
        return java_match.group(1)
    elif python_match:
        return python_match.group(1)
    elif js_match:
        return js_match.group(1)
    else:
        return False
    


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
                if (re.search(r'\bversion\b', answer) or re.search(r'\bversion\b', answer)):
                    if ((capture_version(answer) or capture_version(prompt))):
                        version_obtained = capture_version(answer)
                        print(version_obtained)
                        relevant_data.append({
                            'Contains_version': True,
                            'content': entry
                        })
                        break


                    
            # print(relevant_data)
    return relevant_data



def save_to_json(data, output_folder, filename):
    output_file_path = os.path.join(output_folder, f"{filename}.json")
    with open(output_file_path, 'w', encoding='utf-8') as output_json:
        json.dump(data, output_json, indent=2)
    print(f"Data saved to {output_file_path}")

def process_files(output_folder):
    file_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contain_lib_code_import_2\pr_sharings.json'
   
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
