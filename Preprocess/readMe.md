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
