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

# gemini_testv2.py

## Overview
This is a text analysis script using the Google Gemini model, primarily designed to identify the most likely article containing the answer to a question from multiple reference documents.

## Main Components
1. **Configuration Settings**
   - Sets file paths for reference documents, questions, and answers
   - Configures the Gemini API key
   - Initializes the Tbrain object

2. **Model Configuration**
   - Utilizes the `gemini-1.5-flash` model
   - Sets up the prompt template

3. **Core Processing Flow**
   - Reads specific questions
   - Constructs a prompt containing the question and reference documents
   - Generates answers using the Gemini model
   - Verifies the correctness of the answer
   - Includes error handling and retry mechanisms

## Special Features
- Multiple API key rotation
- Detailed error logging
- Dynamic adjustment of temperature parameter
- Answer evaluation and storage

## Error Handling
- Automatic API key switching on errors
- Retries up to 2 times
- Detailed error information saved in the `Error_detail` directory

## Output
- Generated answers (article IDs)
- Evaluation results
- Detailed error logs (if applicable)
