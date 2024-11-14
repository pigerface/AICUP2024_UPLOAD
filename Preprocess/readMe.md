# AIcupPDFtoText.py

## Overview
The `AIcup_pdf_to_text` module is designed to convert PDF files into text, supporting various OCR and text processing methods to ensure accurate document extraction and storage. Key functions include mounting Google Drive, performing OCR, converting PDFs to text, batch processing files, and uploading to the OpenAI API for format cleanup.

### Key Functions
1. **Google Drive Mounting**
   - Mounts Google Drive, allowing files to be read from and saved to specified paths.

2. **OCRmyPDF Installation and Execution**
   - Installs necessary dependencies for OCR, such as `tesseract-ocr` and `JBIG2 encoder`.
   - Executes `ocrmypdf` to perform OCR on PDF files, supporting English and Traditional Chinese, and saves the output as a text file.

3. **PDF Text Conversion**
   - Uses `pdftotext` to convert PDFs to text format, saving the output to a specified location.
   - If the text length is unusually short, the conversion is deemed unsuccessful and further processed with OCR.

4. **Batch Processing of All PDFs in a Folder**
   - Iterates through specified folders, performing text conversion or OCR on each PDF file.
   - Saves results in a designated output folder.

5. **OpenAI API Cleanup and Organization**
   - Uploads PDFs to the OpenAI API for format reference.
   - Sends extracted text to OpenAI for format cleanup, fixing OCR-induced formatting issues.

6. **Simple OCR Processing**
   - Installs `easyocr` for handling inaccurate OCR, using `pdf2image` for image conversion.
   - Utilizes multithreading to process pages in batches, enhancing efficiency for large files.

## Key Features
- **Supports OCR for Traditional Chinese and English**
- **Identifies and handles failed PDF-to-text conversions**
- **Integrates OpenAI API for format correction**
- **Processes large files using multithreading for improved efficiency**
- **Batch processes entire folders for time efficiency**

# TBrain.py 

## Overview
The `TBrain.py` module is designed for processing and evaluating the TBrain dataset, comprising three main classes:

### 1. Question - Question Data Handler
   - Stores question ID, category, content, and choices
   - Tracks answer status for each question

### 2. Reference - Reference Document Handler
   - Manages reference document ID, category, and content
   - Provides formatted document display

### 3. Tbrain - Core Management Class
   - Handles dataset loading and preprocessing
   - Manages answer submissions
   - Provides evaluation functionality
   - Manages file I/O operations

## Key Features
- **Reading and processing reference documents**
- **Loading and managing question data**
- **Handling answer submissions**
- **Evaluating answer accuracy**
- **Generating output results**
  
# store_sumamry.py

## Overview
This script generates summaries for articles by utilizing Google's Gemini AI model. It processes text files within a specified directory, generates summaries for each article, and saves them in a separate directory structure that mirrors the original categorization.

## Main Components
1. **Configuration Settings**
   - Defines paths for reference directories, questions, outputs, and summaries
   - Configures Gemini API keys
   - Initializes the Gemini model

2. **Processing Workflow**
   - Walks through a directory of text files
   - Constructs a prompt with specific instructions for summarizing articles
   - Generates summaries using the Gemini model
   - Skips files if a summary already exists
   - Handles Chinese calendar year conversion and removes numerical data from financial reports

3. **Special Instructions**
   - Converts Chinese calendar years to the Gregorian calendar format
   - Excludes numerical data from summaries of financial reports

## Key Features
- **Multi-API Key Rotation**: Automatically switches API keys on error to ensure continuous processing.
- **Directory-Based Text File Processing**: Reads text files from the specified reference directory.
- **Summary Generation**: Creates summaries while preserving the original article IDs.
- **Error Handling with Retry Mechanism**: Pauses and retries on API errors, with a 10-second delay between retries.
