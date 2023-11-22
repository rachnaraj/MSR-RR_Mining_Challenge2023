import os
import json

# Set the path to the folder containing your JSON files
folder_path = 'D:\\Me\\concordia\\Notes\\Prof-Diego\\MSR-DataChallenge\\Extracted-Dataset\\Store-Extracted-Files'


# Create an empty list to store the data from each file
all_data = []

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        # Construct the full path to the file
        file_path = os.path.join(folder_path, filename)

        # Read the JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Append the data to the list
        all_data.append(data)

# Combine all the data into a single dictionary or list
# Depending on your data structure, you may need to modify this part
combined_data = {'all_data': all_data}

# Set the path to the output combined JSON file
output_file_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Extracted-Dataset\Store-Extracted-Files/Combined-file.json'

# Write the combined data to the output file
with open(output_file_path, 'w') as output_file:
    json.dump(combined_data, output_file, indent=2)

print(f'Combined JSON file saved to {output_file_path}')
