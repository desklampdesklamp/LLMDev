# LLM Development Testing - README

## Overview
This repository contains a simple Python-based chat application utilizing a large language model (LLM) for generating responses. The application is built with a focus on easy testing and development of chatbot functionalities.

## Code Structure
The codebase consists of three primary files:

1. **app.py**: This is the main executable script for running the chat application. It initializes the chat, handles user input, and manages the chat session.

2. **chat.py**: Contains functions related to initializing the chat model and generating responses using the LLM.

3. **memory.py**: Manages the loading and saving of chat messages in JSON format, along with some utility functions for handling messages.

## Dependencies
- Python 3.11.5
- conda

To install the necessary libraries, run:
```bash
conda env create -f environment.yml -n LLMdev
```

## Usage
To run the chat application, execute the `app.py` script:
```bash
python app.py
```
**app.py**
This script initializes the chat environment and handles the main chat loop. User inputs are taken, processed by the LLM, and responses are generated and displayed. The conversation is saved in JSON format.

**chat.py**
Handles the initialization of the LLM and the generation of responses. It uses the transformers library for the LLM functionality. The extract_code function is used for extracting code blocks from markdown outputs.

**memory.py**
Manages the reading and writing of chat messages to and from JSON files. It includes error handling for file operations and JSON serialization issues.

## Development and Testing

For development and testing purposes:

1. Modify `app.py`, `chat.py`, or `memory.py` as needed.
2. Run `app.py` to test the changes in real-time.
