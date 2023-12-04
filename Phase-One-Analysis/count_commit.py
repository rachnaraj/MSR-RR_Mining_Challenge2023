import json
import os
import glob 

def extract_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        relevant_conversations_count = 0
        for source in data.get('Sources', []):
            source_type = source.get('Type', '')
            for chatgpt_sharing in source.get('ChatgptSharing', []):
                if chatgpt_sharing.get('Conversations'):
                    for conversation in chatgpt_sharing['Conversations']:
                        relevant_conversations_count +=1
                        

                            
        print(relevant_conversations_count)
                

    return relevant_conversations_count

def process_files(base_folder, file_pattern):
    file_paths = [f for f in glob.glob(os.path.join(base_folder, 'snapshot*', '**', file_pattern), recursive=True)]
    total_relevant_data = 0
    for file_path in file_paths:
        relevant_data = extract_info(file_path)
        total_relevant_data += relevant_data
    print(f"All files processed, total count is: {total_relevant_data}")

if __name__ == "__main__":
    base_folder = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\New-Dataset\DevGPT'
    # output_folder_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge'  # Replace with the desired output folder
    file_pattern = '*_commit_sharings.json'
    # Process all JSON files in the input folder and save with different names in the output folder
    process_files(base_folder, file_pattern)
