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
def extract_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        relevant_conversations = []
        for source in data.get('Sources', []):
            source_type = source.get('Type', '')
            Author = source.get('Author', '')
            RepoName = source.get('RepoName', '')
            Title = source.get('Title', '')
            Body = source.get('Body', '')
            State = source.get('State', '')
            
            
            for chatgpt_sharing in source.get('ChatgptSharing', []):
                if chatgpt_sharing.get('Conversations'):
                    gpt_URL = chatgpt_sharing.get('URL', '')
                    NumberOfPrompts = chatgpt_sharing.get('NumberOfPrompts', '')
                    gpt_model_version = chatgpt_sharing.get('Model', '')
                    for conversation in chatgpt_sharing['Conversations']:
                        if conversation.get('ListOfCode') != []:
                            # Check if any code block in the conversation meets the condition
                            if any(
                                'Type' in code_block and
                                re.search(r'\bimport\b', code_block.get('Content', '')) and
                                code_block['Type'] in ['java', 'javascript', 'python', 'typescript']
                                for code_block in conversation.get('ListOfCode', [])
                            ):
                                unique_id = generate_unique_id()
                                relevant_conversations.append({
                                    'ID': unique_id,
                                    'source_type': source_type,
                                    'Author': Author,
                                    'SourceURL' : gpt_URL,
                                    'RepoName' : RepoName,
                                    'Title' : Title, 
                                    'Body': Body,
                                    'State':State,
                                    'NumberOfPrompts':NumberOfPrompts,
                                    'gpt_model_version':gpt_model_version,
                                    'Conversation':  chatgpt_sharing['Conversations']
                                })
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
    file_path = r"D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Dataset_v9\DevGPT\snapshot_20231012\20231012_235128_issue_sharings.json"
   
    relevant_data = extract_info(file_path)
    # print("&&&&&&&&&&&&&&&&&&&&&&&&&&" , relevant_data)
    if relevant_data:
        print("count is:",len(relevant_data))
        save_to_json(relevant_data, output_folder, 'issue_sharings')
    else:
        print("No relevant data found!")
    print(f"All files processed.")
if __name__ == "__main__":
    output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\git-folder-MSR\MSR-RR_Mining_Challenge2023\Data_Creation\Contains_library_code_import'
    process_files(output_folder_path)