"""
A script to generate summaries of articles using Google's Gemini AI model.

This script walks through a directory of text files, processes each article,
and generates a summary using the Gemini model. The summaries are stored in 
a separate directory structure maintaining the original categorization.

Key features:
- Handles multiple API keys with rotation on failure
- Processes text files from specified directory
- Generates summaries while preserving article IDs
- Handles Chinese calendar year conversion
- Removes numerical data from financial reports
"""


import google.generativeai as genai
from tbrain import Tbrain
from  tbrain import Tbrain
import os
import time
REFERENCE_DIR_PATH = "../Preprocessed/reference_preprocessed/"
QUESTION_JSON_PATH = "../Preprocessed/questions_example.json"
OUTPUT_JSON_PATH = "output.json"
TRUTH_JSON_PATH = "../Preprocessed/ground_truths_example.json"
SUMMARY_DIR_PATH = "../Preprocessed/summary/"
API_KEY_LIST = ["API_KEY1", "API_KEY2"] # add your own API key here
api_key_index = 20
genai.configure(api_key=API_KEY_LIST[api_key_index])

model = genai.GenerativeModel('gemini-1.5-flash')

first_instruction = """
從現在開始，我會一個較長的文章。你的任務是為對文章進行總結。\n\n
輸入的格式是：\n
=== 文章 <文章編號 A> 開始 ===\n
<文章內容，可能有很多行>\n
=== 文章 <文章編號 A> 結束 ===\n\n
...\n
\n
文章編號是隨機的，你必須為每個文章的內容作出總結，把重點提取出來，\n
若文件內容為財報，移除財報內的數字，只保留時間資訊
將年份為民國年，在民國年後加上西元年\n

輸出的格式是：\n
=== 文章 <文章編號 A> 摘要開始 ===\n
<文章 A 總結過後的內容>\n
=== 文章 <文章編號 A> 摘要結束 ===\n\n
...\n
現在開始：\n\n 
"""

for root, _, files in os.walk(REFERENCE_DIR_PATH):
    for file in sorted(files):
        file_path = os.path.join(root, file)
        category = os.path.basename(os.path.dirname(file_path))
        # if category in ['insurance', 'finance']:
        #     continue
        if file_path.endswith('.txt'):
            ref_id = os.path.splitext(file)[0]
            # if ref_id == '12':
            #     continue
            print(f'{category} {ref_id}')
            summary_path = os.path.join(f'summary/{category}', f"{ref_id}.txt")
            if os.path.exists(summary_path):
                with open(summary_path, 'r') as file:
                    print(f'{summary_path} exists')
                    continue
                    # if file.read().strip() == '':
                    #     continue
            prompt = first_instruction
            if os.path.isfile(file_path) and ref_id.isdigit():
                with open(file_path, 'r') as file:
                    content = file.read()
                    prompt += f"=== 文章 {ref_id} 開始 ===\n"
                    prompt += content + "\n"
                    prompt += f"===  文章 {ref_id} 結束 ===\n\n\n\n"
                    try:
                        response = model.generate_content(prompt)
                        print(f'response: {response.text}')
                    except:
                        print(f'key_index: {api_key_index}')
                        api_key_index = (api_key_index + 1) % len(API_KEY_LIST)
                        genai.configure(api_key=API_KEY_LIST[api_key_index])
                        # wait 10 seconds
                        time.sleep(10)
                        continue
                    
                    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
                    with open(summary_path, 'w') as file:
                        file.write(response.text)
