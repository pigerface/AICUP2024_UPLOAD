# -*- coding: utf-8 -*-

import subprocess
import os
import pdftotext

def ocr_and_clean_document(input_pdf_path, output_txt_path):
    """
    Performs OCR on a PDF file and extracts the text content.
    
    Args:
        input_pdf_path (str): Path to the input PDF file
        output_txt_path (str): Path where the extracted text will be saved
        
    Returns:
        str: The stderr output from the OCR process
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


def read_pdf_and_save(file_path, output_path):
    """
    Reads a PDF file and saves its text content to a file.
    
    Args:
        file_path (str): Path to the PDF file to read
        output_path (str): Path where the extracted text will be saved
        
    Returns:
        int: -1 if the extracted content length is > 100, otherwise returns the content length
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

def process_pdfs_in_folder(input_folder_path, output_folder_path):
    """
    Processes all PDF files in a folder by extracting their text content.
    
    The function first attempts to extract text directly using pdftotext.
    If that fails (resulting in short content), it falls back to OCR processing.
    
    Args:
        input_folder_path (str): Path to the folder containing PDF files
        output_folder_path (str): Path where the extracted text files will be saved
        
    Returns:
        None
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
io_folder = {"/AIcup_dataset/reference/insurance":"/output/insurance", "/AIcup_dataset/reference/finance":"/output/finance"}   # Folder where PDFs are stored
for i , o in io_folder.items():
  print("Now processing pdf :", i)
  print("Output file will be in: ", o)
  process_pdfs_in_folder(i, o)

