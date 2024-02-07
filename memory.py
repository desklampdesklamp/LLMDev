import json
import logging
import os

def load_memory(file_path, default_data=None):
    """
    Loads chat memory from a JSON file.

    Parameters:
    - file_path (str): Path to the JSON file.
    - default_data (optional): Default data to return in case of error.

    Returns:
    - list or None: The chat memory data or None/default_data if an error occurs.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                logging.error(f"JSON file does not contain a list: {file_path}")
                return default_data
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in file: {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")

    return default_data

def save_message(messages, filename):
    """
    Saves chat messages to a JSON file.

    Parameters:
    - messages (list): List of chat messages to save.
    - filename (str): Path to the JSON file where messages will be saved.

    Raises:
    - TypeError: If the input messages are not JSON-serializable.
    - IOError: If an I/O error occurs while writing the file.
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Writing the JSON-serializable list to a file
        with open(filename, 'w') as file:
            json.dump(messages, file, indent=4)

    except TypeError as e:
        logging.error(f"Input is not a JSON-serializable list: {e}")
        raise TypeError(f"Input is not a JSON-serializable list: {e}")
    except IOError as e:
        logging.error(f"Error occurred in file writing: {e}")
        raise IOError(f"Error occurred in file writing: {e}")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        raise Exception(f"Unexpected error occurred: {e}")
    
def create_message(role,content):
    """
    Creates a chat message in JSON format.

    Parameters:
    - role (str): The role of the message sender (e.g., "user" or "assistant").
    - content (str): The content of the message.

    Returns:
    - dict: A dictionary representing the message.
    """
    message = {"role":role,"content":content}
    return message


def combine_message_files(filenames, combined_filename):
    """
    Combine messages from multiple JSON files into a single file.

    Arguments:
    - filenames: List of filenames to combine.
    - combined_filename: The filename for the combined output.
    """
    combined_messages = []
    for filename in filenames:
        with open(filename, 'r') as file:
            messages = json.load(file)
            combined_messages.extend(messages)
    
    with open(combined_filename, 'w') as file:
        json.dump(combined_messages, file, indent=4)
        
def preprocess_and_correct_json_string(json_str):
    # Attempt to correct a specific formatting error
    corrected_str = json_str.replace("\\_", "_")
    
    # Try to parse the corrected string as JSON
    try:
        parsed_json = json.loads(corrected_str)
        # If successful, return the corrected and parsed JSON as a string
        return json.dumps(parsed_json)
    except json.JSONDecodeError:
        # If it's not valid JSON, return the original string
        return json_str