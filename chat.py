from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import torch

def initialize_chat(model_name="mistralai/Mistral-7B-Instruct-v0.2", device="auto"):
    """
    Initializes the chat model and tokenizer.

    Parameters:
    - model_name (str): Identifier for the model to be loaded.
    - device (str): The device to run the model on ("cuda:X", "cpu", or "auto").

    Returns:
    - tuple: Contains an empty initial message list, the loaded model, tokenizer, and device configuration.
    """
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = device  # Use the specified device

    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

def generate_response(messages, model, tokenizer, device):
    """
    Generates a chat response based on the provided messages.

    Parameters:
    - messages (list): List of chat messages.
    - model: The loaded chat model.
    - tokenizer: The tokenizer for the model.
    - device (str): The device to run the model on.

    Returns:
    - str: The generated response.
    """
    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
    
    input_prompt = tokenizer.batch_decode(encodeds)
    input_len = len(input_prompt[0])
    
    model_inputs = encodeds.to(device)
    model.to(device)

    generated_ids = model.generate(model_inputs, max_new_tokens=8000, do_sample=True, pad_token_id=tokenizer.eos_token_id)
    decoded = tokenizer.batch_decode(generated_ids)
    response = decoded[0]
    
    assistant_answer = response[input_len:-4]
    
    return assistant_answer