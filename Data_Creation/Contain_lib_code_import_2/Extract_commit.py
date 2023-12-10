import json
import os
import glob
import re
# Global variable for unique ID
id_counter = 0

def generate_unique_id():
    global id_counter
    id_counter += 1
    return id_counter


def contains_install_keywords(text):
    install_keywords = ["pip install", "conda install", "npm install", "mvn install"]
    return any(keyword in text for keyword in install_keywords)


def extract_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    relevant_conversations = []
    
    for entry in data:
        
        if isinstance(entry, str):
            try:
                entry = json.loads(entry)
            except json.JSONDecodeError:
                # Handle the case where the string cannot be parsed as JSON
                continue

        if isinstance(entry, dict):
            conversations = entry.get("Conversation", [])
        
            for conversation in conversations:
                # print("entering!!!")
                prompt = conversation.get('Prompt', '')
                answer = conversation.get('Answer', '')
                list_of_code = conversation.get('ListOfCode', [])
                if any(
                    code_block['Type'] in ['java', 'javascript', 'python', 'typescript']
                    for code_block in conversation.get('ListOfCode', [])
                ):
                    for code_block in conversation.get('ListOfCode', []):
                        prompt = conversation.get('Prompt', '')
                        # print(prompt)
                        answer = conversation.get('Answer', '')
                        if re.search(r'\bimport\b',answer) or re.search(r'\bimport\b',prompt) or re.search(r'\bimport\b',code_block['Content']) or re.search(r'\require\b',code_block['Content']) or contains_install_keywords(answer) or contains_install_keywords(prompt):
                                   
                            relevant_conversations.append(
                                entry
                                
                            )
                            break
                    break

            
            
                            
    return relevant_conversations

def save_to_json(data, output_folder, filename):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the output folder if it doesn't exist

    output_file_name = f"{filename}.json"
    output_file_path = os.path.join(output_folder, output_file_name)

    with open(output_file_path, 'w', encoding='utf-8') as output_json:
        json.dump(data, output_json, indent=2)
    
    print(f"Data saved to {output_file_path}")

# ...

def process_files(output_folder):
    file_path = r"D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\contains_conversations_of_code\commit_sharings_.json"
   
    relevant_data = extract_info(file_path)
    # print("&&&&&&&&&&&&&&&&&&&&&&&&&&" , relevant_data)
    if relevant_data:
        print("count is:",len(relevant_data))
        save_to_json(relevant_data, output_folder, 'commit_sharings')
    else:
        print("No relevant data found!")
    print(f"All files processed.")



if __name__ == "__main__":
    output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contain_lib_code_import_2'
    process_files(output_folder_path)
