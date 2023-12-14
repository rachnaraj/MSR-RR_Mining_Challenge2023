# MSR-RR_Mining_Challenge2023 
Link: https://2024.msrconf.org/track/msr-2024-mining-challenge
**Data Exploration task**
This study aims to understand the role of library versions in developer-ChatGPT interactions. 
To that aim, we mine the DevGPT dataset, a dataset of Developer-ChatGPT conversations with more than 2,000 conversations.  
DevGPT was created by mining links to ChatGPT conversations shared by developers using the OpenAI sharing functionality https://help.openai.com/en/articles/7925741-chatgpt-shared-links-faq
The dataset is a collection of JSON files covering the interaction metadata, prompts asked and answers from ChatGPT, including text and code snippets.

# Dataset Details & Download Link:
Details: https://github.com/NAIST-SE/DevGPT
Link: https://zenodo.org/records/8304091

##Dataset Version used in this project:
Version 9 (Snapshots_20231012)

#Steps To Execute the Project:
1. Download the mentioned version, store it in the local directory.
2. Cloan Project using the below command.
    ```bash
    
    git clone https://github.com/rachnaraj/MSR-RR_Mining_Challenge2023.git
    
    ```
3. Open a particular python file and update the dataset reference to an appropriate path.

    ```
    
    file_path = r'D:\Me\concordia\Notes\Prof-Diego\MSR-DataChallenge\Implementation\Dataset_v9\DevGPT\snapshot_20231012\20231012_235320_discussion_sharings.json'
    
    ```
4. Execute the python script.

#About files:
Each file is a fileteration step of DevGPT Dataset.

1. contains_conversations_on_code_general

   This folder filters all conversations where ChatGPT has recommended some code to the user (Developer)

2. contains_conversations_of_code
   This folder filters all conversations where ChatGPT has recommended some code in Java, Python, Javascript and Typescript programming language.

4. Contain_lob_code_import_2

   This folders filters conversations where ChatGPT is suggestion some code of libraries.
   Since we focused on code-related conversations from Java, Python, and Javascript, we resort to identifying when libraries are imported in those languages. We focused on how open source libraries and rendered in these languages. 
   These languages allow developers to import libraries by using the special keyword {import} in the code. We also considered the keyword {require} for JavaScript related code, a more versatile method for importing libraries. We search for these two keywords in the code snippet of all conversations, and include a conversation if one or more code snippets included      any dependency.

6. Contains_download_suggestions
  This folder contains conversations where ChatGPT has suggested some code to download the open source library.
  Note that, while we coined conversations as "library-related", the conversations are not necessarily primarily about libraries.
  A user may ask ChatGPT to help them write a function to export content to a PDF file (the focus of the conversation), in which ChatGPT is likely to recommend a library that embeds that functionality (support role for the conversation).
  On the other hand, when ChatGPT explicitly mentions the need for installing a specific library, we expect library versions to play a more significant role. 
  To investigate this hypothesis, we also filter conversations where ChatGPT explicitly recommends users install libraries. 
  We filter conversations that have, in at least one interaction, ChatGPT recommending users to install new libraries through the commands: ``pip install'', ``conda install'', ``npm install'', or ``mvn install'', and these are the de-facto methods for installing libraries in the targeted programming languages.
   

8. Contains_version(regex)
   This folder contains conversations where library versions were mentioned bu user or by ChatGPT.
   To capture conversations that include at least a single mention of library versions, we employ a regex that captures semantic versioning specifications.

   
10. Contains_version_and_download_suggestion
    This folder filters those conversation where semantic versions and download recommendations are captured.




