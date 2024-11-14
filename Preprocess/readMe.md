# aicup_pdf_to_text.py

## Overview
This script processes PDF documents by first attempting direct text extraction using `pdftotext`. If the direct extraction results in insufficient content, it falls back to OCR using `ocrmypdf` to retrieve text from scanned PDFs. Extracted text is then saved in a specified output directory, preserving the original categorization.

## Main Components
1. **OCR and Text Cleaning Function (`ocr_and_clean_document`)**
   - Performs OCR on a PDF file if direct extraction fails.
   - Saves the OCR output to a text file.

2. **PDF Reading Function (`read_pdf_and_save`)**
   - Reads and extracts text from PDF files using `pdftotext`.
   - Verifies content length to determine if OCR fallback is necessary.

3. **Folder Processing Function (`process_pdfs_in_folder`)**
   - Iterates through all PDF files in the specified folder.
   - Uses direct text extraction as the primary method.
   - Falls back to OCR if content is too short, indicating extraction failure.

## Special Instructions
- **Fallback to OCR**: If `pdftotext` fails (producing short content), the script switches to OCR.
- **Error Handling**: Detailed OCR process logs are displayed, and errors during OCR are captured.
- **Directory Management**: Automatically creates output folders if they do not exist.

## Key Features
- **OCR and Direct Extraction Hybrid**: Automatically switches between direct text extraction and OCR based on content length.
- **Automated Directory Processing**: Handles all PDFs within specified directories.
- **Structured Output**: Saves extracted text with the original PDF filenames (in `.txt` format) for easy reference.


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

# setup.sh

## Overview
This bash script sets up an environment for performing OCR on PDF documents using OCRmyPDF and Tesseract OCR. Additionally, it installs dependencies for JBIG2 encoding, which is used by OCRmyPDF for more efficient compression of scanned PDF images.

## Script Steps

1. **System Update**
   - Updates the package list to ensure all packages are up-to-date.

2. **Install OCRmyPDF and Tesseract OCR**
   - Installs `ocrmypdf` for PDF OCR processing.
   - Installs `tesseract-ocr` with support for traditional Chinese (`tesseract-ocr-chi-tra`).

3. **Install JBIG2 Encoder Dependencies**
   - Installs necessary development tools and libraries required to build and run the JBIG2 encoder.

4. **Clone and Build JBIG2 Encoder**
   - Clones the JBIG2 encoder repository from GitHub.
   - Builds and installs the encoder to optimize OCRmyPDF's processing efficiency.

5. **Install Additional Libraries and Tools**
   - Installs essential development tools like `build-essential`, `libpoppler-cpp-dev`, and other dependencies for handling PDFs and building packages.

6. **Install Python Package for PDF Text Extraction**
   - Installs the `pdftotext` Python package, enabling direct text extraction from PDFs.

## Key Features
- **Multi-Language OCR**: Includes support for both English and Traditional Chinese text recognition.
- **Efficient Compression**: Sets up JBIG2 encoding for optimized PDF compression.
- **Full Development Environment**: Installs additional libraries to support PDF processing and development tasks.
