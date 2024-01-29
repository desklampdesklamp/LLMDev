from transformers import AutoModelForCausalLM, AutoTokenizer
import re
import os
from typing import Tuple

def initialize_chat():
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
    device = "cuda"
    initial_message = []
    messages = initial_message
    return messages, model, tokenizer, device

def generate_response(messages, model, tokenizer, device):
    #takes in a message and returns a response
    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
    
    input_prompt = tokenizer.batch_decode(encodeds)
    input_len = len(input_prompt[0])
    
    model_inputs = encodeds.to(device)
    model.to(device)

    generated_ids = model.generate(model_inputs, max_new_tokens=8000, do_sample=True, pad_token_id=tokenizer.eos_token_id)
    decoded = tokenizer.batch_decode(generated_ids)
    reponse = decoded[0]
    
    assistant_answer = reponse[input_len:-4]
    
    return assistant_answer

def extract_code(output: str, filename: str = 'code.py', folder: str = 'tools') -> Tuple[bool, str]:
    """
    Parses markdown output to extract code blocks and saves them to a specified file in a given folder.
    
    Parameters:
    output (str): Markdown text to parse.
    filename (str): Name of the file to save the code. Defaults to 'code.py'.
    folder (str): Folder to save the file. Defaults to 'tools'.

    Returns:
    Tuple[bool, str]: A tuple containing a boolean indicating success or failure, and a message.
    """
    code_pattern = re.compile(r'```(?:\w+\n)?([\s\S]+?)```', re.DOTALL)
    matches = code_pattern.findall(output)

    if matches:
        # Create the folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Construct the file path
        file_path = os.path.join(folder, filename)

        try:
            with open(file_path, 'w') as f:
                for code in matches:
                    f.write(code + '\n\n')
            return True, f'Successfully extracted code blocks to {file_path}.'
        except IOError as e:
            return False, f'File writing error: {e}'
    else:
        return False, 'No code blocks found in the markdown output.'


    return message
