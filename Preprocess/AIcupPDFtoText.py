# -*- coding: utf-8 -*-
"""AIcup_pdf_to_text

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y2EzKLrhbFHPeWfefd7CN7GewQsoZzLF
"""

from google.colab import drive
drive.mount('/content/drive/')

# # ---------Instal OCRmyPDF---------
# ! sudo apt install tesseract-ocr
# ! sudo apt-get install tesseract-ocr-chi-tra
# ! sudo apt install ocrmypdf
# ! apt-cache search tesseract-ocr

# # Commented out IPython magic to ensure Python compatibility.
# # ----- Install JBIG2 encoder for OCRmyPDF -----
# ! sudo apt install autotools-dev automake libtool libleptonica-dev # install JBIG2 encoder dependencies
# ! git clone https://github.com/agl/jbig2enc
# ! sleep 5
# ! pwd
# # %cd jbig2enc
# ! ./autogen.sh
# ! ./configure && make
# ! sudo make install # build JBIG2 encoder to source
# # %cd ..

import subprocess
import os

def ocr_and_clean_document(input_pdf_path, output_txt_path):
    """
    Performs OCR on a PDF document and extracts the text content.
    
    Args:
        input_pdf_path (str): Path to the input PDF file
        output_txt_path (str): Path where the extracted text will be saved
        
    Returns:
        str: Standard error output from the OCR process
    """

    # Step 1: Execute the OCR command
    # ocr_command = f"ocrmypdf -l eng+chi_tra --force-ocr --sidecar {output_txt_path} {input_pdf_path} output.pdf"
    ocr_command = f"ocrmypdf -l eng+chi_tra --force-ocr --sidecar {output_txt_path} {input_pdf_path} output.pdf"
    result = subprocess.run(ocr_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

    print(f"OCR completed. Text extracted to {output_txt_path}")

    # Step 2: Read the extracted text from the file
    with open(output_txt_path, 'r', encoding='utf-8') as file:
        extracted_text = file.read()

    return result.stderr


# Example usage
if __name__ == '__main__' :
    input_pdf_path = "all_scan.pdf"
    output_txt_path = "ocrmypdf.txt"

    print(ocr_and_clean_document(input_pdf_path, output_txt_path))

# ! sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev
# ! pip install pdftotext

import pdftotext

def read_pdf_and_save(file_path, output_path):
    """
    Extracts text from a PDF file using pdftotext and saves it to a file.
    
    Args:
        file_path (str): Path to the input PDF file
        output_path (str): Path where the extracted text will be saved
        
    Returns:
        int: -1 if extracted content length > 100, otherwise returns content length
    """

    # Load the PDF file
    with open(file_path, "rb") as f:
        pdf = pdftotext.PDF(f)

    # Convert the PDF content to a single string, joining pages with new lines
    pdf_content = "\n\n".join(pdf)

    # Save the extracted text to the output file
    with open(output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(pdf_content)

    print(f"PDF content saved to {output_path}")
    return -1 if len(pdf_content)>100 else len(pdf_content)


# Example usage:
if __name__ == '__main__' :
    input_pdf_path = "all_scan.pdf"
    output_text_path = "pdftotext.txt"
    print(read_pdf_and_save(input_pdf_path, output_text_path))

"""Transform logic"""

import os

def process_pdfs_in_folder(input_folder_path, output_folder_path):
    """
    Processes all PDF files in a folder using OCR or direct text extraction.
    
    Args:
        input_folder_path (str): Directory containing PDF files to process
        output_folder_path (str): Directory where extracted text files will be saved
    """
    # Ensure the output folder exists
    os.makedirs(output_folder_path, exist_ok=True)

    # Iterate through all files in the input folder
    for file_name in os.listdir(input_folder_path):
        # Process only .pdf files
        if file_name.endswith('.pdf'):
            print("Processing file:", file_name )
            input_pdf_path = os.path.join(input_folder_path, file_name)

            # Create output path in the output folder with the same filename but .txt extension
            output_txt_path = os.path.join(output_folder_path, file_name.replace('.pdf', '.txt'))

            # Check if the result contains "page already has text!"
            pdf_len = read_pdf_and_save(input_pdf_path, output_txt_path)
            if pdf_len != -1 :
                print(f"PDF content too short, len : {pdf_len} ,maybe pdftotext failed, use OCR")
                # Call the OCR and cleaning function
                result = ocr_and_clean_document(input_pdf_path, output_txt_path)
                print("OCR logs:\n", result)

            else:
                pass
    print("Folder scanned")


# Example usage
io_folder = {"/content/drive/MyDrive/AIcup_dataset/reference/insurance":"/content/output/insurance", "/content/drive/MyDrive/AIcup_dataset/reference/finance":"/content/output/finance"}   # Folder where PDFs are stored
for i , o in io_folder.items():
  print("Now processing pdf :", i)
  print("Output file will be in: ", o)
  process_pdfs_in_folder(i, o)

# Commented out IPython magic to ensure Python compatibility.
# %cp -av output /content/drive/MyDrive/AIcup_dataset/output

"""# OpenAi API organizer (Too expensive)"""

# ! pip install openai
from openai import OpenAI
from pathlib import Path

from google.colab import userdata
client = OpenAI(
    # This is the default and can be omitted
    api_key=userdata.get('OPENAI_API_KEY')
)

def upload_pdf_to_openai(file_path):
    """
    Uploads a PDF file to OpenAI API for processing.
    
    Args:
        file_path (str): Path to the PDF file to upload
        
    Returns:
        str: File ID from OpenAI API if successful, None if upload fails
    """
    try:
        response = client.files.create(
            file=open(file_path,"rb"),
            purpose="assistants" # Purpose can vary depending on the API use case
        )
        return response.id
    except Exception as e:
        print(f"Error occurred while uploading the PDF: {e}")
        return None

# Step 3: Upload the PDF to OpenAI for reference
pdf_file_id = upload_pdf_to_openai(input_pdf_path)
if not pdf_file_id:
    print("PDF upload failed, proceeding without PDF reference.")

# Step 4: Send the text to OpenAI to clean the document
system_prompt = "You are an expert at cleaning and organizing OCR scanned files. The content of OCR is correct. Your job is to fix formatting issues, apart from formatting, do not modify any content. The uploaded PDF is only for format reference, please produce an output in the same language as the uploaded PDF"

agent = client.beta.assistants.create(
model="gpt-4o",
name="Agent",
instructions=system_prompt,
tools=[{"type": "file_search"}],
)
thread = client.beta.threads.create()
print(thread)

message = client.beta.threads.messages.create(
thread_id=thread.id,
role="user",
content=extracted_text,
attachments=[
    {
    "file_id": pdf_file_id,
    "tools": [{ "type": "file_search" }],
    }
],
)
print(message)
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=agent.id,
)
print(run)
all_messages = client.beta.threads.messages.list(
thread_id=thread.id
)
print(all_messages.data[0].content[0].text.value)
cleaned_text = all_messages.data[0].content[0].text.value

# Step 5: Write the cleaned text back into the file
with open(output_txt_path, 'w', encoding='utf-8') as file:
    file.write(cleaned_text)

print(f"Document cleaned and saved to {output_txt_path}")

"""# Inaccurate OCR"""

# ! pip install PyPDF2 pdf2image Pillow numpy easyocr tqdm
# ! sudo apt-get install -y poppler-utils
# ! sudo apt install libtesseract-dev
import easyocr
import pdf2image
from PyPDF2 import PdfReader
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os
import numpy as np

def get_num_pages(pdf_path):
    """
    Gets the total number of pages in a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        int: Number of pages in the PDF
    """
    reader = PdfReader(pdf_path)
    return len(reader.pages)

def process_pages(pdf_path, page_numbers):
    """
    Processes specific pages from a PDF file using EasyOCR.
    
    Args:
        pdf_path (str): Path to the PDF file
        page_numbers (list): List of page numbers to process
        
    Returns:
        dict: Dictionary mapping page numbers to extracted text
    """
    reader = easyocr.Reader(['en', 'ch_tra'], gpu=True)
    images = pdf2image.convert_from_path(pdf_path, dpi=250, first_page=page_numbers[0], last_page=page_numbers[-1])
    text_pages = {}

    for i, image in enumerate(images, start=page_numbers[0]):
        # Convert PIL Image to numpy array
        np_image = np.array(image)
        result = reader.readtext(np_image)
        text = ' '.join([res[1] for res in result])
        print(f"\nPage {i} Text:\n{text}")  # Print recognized text
        text_pages[i] = text + "\n"

    return text_pages

def extract_text_from_pdf(pdf_path, num_pages, batch_size=5):
    """
    Extracts text from a PDF file using parallel processing.
    
    Args:
        pdf_path (str): Path to the PDF file
        num_pages (int): Total number of pages to process
        batch_size (int, optional): Number of pages to process in each batch. Defaults to 5.
        
    Returns:
        str: Concatenated text from all pages
    """
    all_text_pages = {}
    max_workers = os.cpu_count() or 4

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for start_page in range(1, num_pages + 1, batch_size):
            page_numbers = list(range(start_page, min(start_page + batch_size, num_pages + 1)))
            futures.append(executor.submit(process_pages, pdf_path, page_numbers))

        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Pages"):
            all_text_pages.update(future.result())

    all_text = "".join(all_text_pages[i] for i in sorted(all_text_pages))
    return all_text

pdf_path = 'e3.pdf'  # Replace with your PDF file path
num_pages = get_num_pages(pdf_path)
extracted_text = extract_text_from_pdf(pdf_path, num_pages)

with open('extracted_text.txt', 'w', encoding='utf-8') as file:
    file.write(extracted_text)

print("Text extraction and saving complete.")