import google.generativeai as genai
from tbrain import Tbrain
from  tbrain import Tbrain
import time
import random

REFERENCE_DIR_PATH = "../Preprocessed/reference_preprocessed/"
QUESTION_JSON_PATH = "../Preprocessed/questions_example.json"
OUTPUT_JSON_PATH = "output.json"
TRUTH_JSON_PATH = "../Preprocessed/ground_truths_example.json"
SUMMARY_DIR_PATH = "../Preprocessed/summary/"

tb = Tbrain(REFERENCE_DIR_PATH, QUESTION_JSON_PATH, OUTPUT_JSON_PATH, SUMMARY_DIR_PATH, TRUTH_JSON_PATH)

API_KEY_LIST = ["API_KEY1", "API_KEY2"] # add your own API key here

genai.configure(api_key=API_KEY_LIST[10])

model = genai.GenerativeModel('gemini-1.5-flash')

instruction = """
從現在開始，我會給你一個問題，和數個較長的文章及他們的重點摘要。你的任務是回答哪個文章中，最有可能找到問題答案的是哪個文章。\n\n
輸入的格式是：\n
=== 問題開始 ===\n
<問題>\n
=== 問題結束 ===\n\n
=== 文章 <文章編號 A> 開始 ===\n
<文章內容，可能有很多行>\n
=== 文章 <文章編號 A> 結束 ===\n\n
=== 文章 <文章編號 B> 開始 ===\n
<文章內容，可能有很多行>\n
=== 文章 <文章編號 B> 結束 ===\n\n
...\n
=== 文章 <文章編號 A> 摘要開始 ===\n
<文章內容，可能有很多行>\n
=== 文章 <文章編號 A> 摘要結束 ===\n\n
=== 文章 <文章編號 B> 摘要開始 ===\n
<文章內容，可能有很多行>\n
=== 文章 <文章編號 B> 摘要結束 ===\n\n
...\n
\n
文章編號是隨機的，你必須回答最有可能找到答案的那個文章的編號，答案只有一個。\n
你只需要輸出文章的編號就可以了，不需要輸出文章的內容，或其他無關的內容。只需要輸出文章編號即可。\n\n
現在開始：\n\n 
"""

api_key_index = 2

# question_id_list = [35, 64, 82, 94, 126]
# question_id_list = [100]
question_id_list = [100]

"""
A script that uses Google's Gemini model to analyze questions and find the most relevant article 
that contains the answer from a set of given articles and their summaries.

This script:
1. Configures the Gemini API with authentication
2. Processes questions and their associated reference articles
3. Generates answers using the Gemini model
4. Handles errors and retries with different API keys
5. Evaluates and saves the results
"""

def get_specific_question(question_id_list):
    """
    Retrieves specific questions based on their IDs.
    
    Args:
        question_id_list (list): List of question IDs to retrieve
        
    Returns:
        list: List of Question objects matching the provided IDs
    """
    
# for cnt, question in enumerate(tb.get_question_list(unsolved_only=True)[68:]):
for cnt, question in enumerate(tb.get_specific_question(question_id_list)):  
    prompt = instruction
    prompt += "=== 問題開始 ===\n" + question.content + "=== 問題結束 ===\n\n"
    for ref_id in question.choices[:]:
        ref = tb.get_reference(question.category, ref_id)
        prompt += f"=== 文章 {ref_id} 開始 ===\n"
        prompt += ref.content + "\n"
        prompt += f"===  文章 {ref_id} 結束 ===\n\n\n\n"
        print(f'question_category: {question.category}, ref_id: {ref_id}')
        summary = tb.get_summary(question.category, ref_id)

    for ref_id in question.choices[:]:
        summary = tb.get_summary(question.category, ref_id)
        prompt += f"=== 文章 {ref_id} 摘要開始 ===\n"
        prompt += summary + "\n"
        prompt += f"===  文章 {ref_id} 摘要結束 ===\n\n\n\n"
    
    print(prompt)
        
    Err_count = 0
    temperature = 0
    while True:
        try:
            response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(temperature=temperature))
            try:
                answer = int(response.text)
            except:
                answer = -1
            print(f'{question.question_id}/{len(tb.get_question_list())} : {answer}')
            # print(f'question_id: {question.question_id}')
            # print(f'true_answer: {tb.truths.answer}')
            if tb.get_answer(question.question_id) == answer:
                print(f'correct')
                break
            else:
                if Err_count >= 2:
                    break
                if Err_count == 0:
                    # save detail into file
                    with open(f'Error_detail/{question.question_id}.txt', 'w') as f:
                        f.write(f'question: {question.content}\n')
                        f.write(f'answer: {answer}\n')
                        f.write(f'true_answer: {tb.get_answer(question.question_id)}\n')
                        # f.write(prompt)
                        f.write(f'============================================\n')
                        f.write(f'answer_document: \n{tb.get_reference(question.category, answer).content}\n')
                        f.write(f'============================================\n')
                        f.write(f'true_answer_document: \n{tb.get_reference(question.category, tb.get_answer(question.question_id)).content}\n')
                        question_2 = "\n\n這是你生成的答案，為何會生成此答案？!"
                        response = model.generate_content(str(prompt) + str(answer) + str(question_2), generation_config=genai.types.GenerationConfig(temperature=temperature))
                        answer_2 = response.text
                        f.write(f'為何會生成此答案？!\n{answer_2}')
                        print(f'answer: {answer_2}')
                Err_count += 1
        except Exception as e:
            print(f"Error: {e}, key_index: {api_key_index}")
            api_key_index = (api_key_index + 1) % len(API_KEY_LIST)
            genai.configure(api_key=API_KEY_LIST[api_key_index])
            temperature = random.uniform(0.0, 1.0)
            time.sleep(17)
    
    tb.answer_question(question.question_id, answer)
    tb.evaluate()

# 35 FUCK