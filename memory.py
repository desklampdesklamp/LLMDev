import json
import logging

def load_memory(file_path, default_data=None):
    """
    Reads a JSON file and returns its contents as a list. In case of an error, 
    such as file not found or invalid JSON format (not a list), it returns default data if provided, 
    or None otherwise. Errors are logged for debugging.

    Parameters:
    file_path (str): A string representing the path to the JSON file.
    default_data (optional): Data to return in case of an error. Defaults to None.

    Returns:
    list or None: A list containing the contents of the JSON file, 
    or None/default_data in case of an error.
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
    Writes a given list to a JSON file. The list must be JSON-serializable.

    Parameters:
    messages (list): A list that is JSON serializable.
    filename (str): The path of the file where the JSON data will be written.

    Returns:
    None: The function writes to a file and does not return anything.

    Raises:
    TypeError: If the input is not a JSON-serializable list.
    IOError: If there's an issue with file writing.
    """
    try:
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
    Create a json message

    Parameters:
    role (str): Specify role "user" or "assistant"
    content (str): message contents

    Returns:
    str: A JSON message
    """
    message = {"role":role,"content":content}
    return message
