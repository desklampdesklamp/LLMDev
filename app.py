import time
import threading
import copy  # For deep copying the messages list
import chat
import memory
import torch

def timing():
    """Returns the current time in seconds since the Epoch."""
    return time.time()

def initial_models():
    models = {}
    tokenizers = {}
    
    devices =["cuda:" + str(device) for device in list(range(torch.cuda.device_count()))]
    for device in devices:
        model, tokenizer = chat.initialize_chat(device=device)
        models[device] = model
        tokenizers[device] = tokenizer
    
    return models, tokenizers, devices

def generate_and_print_response(prompt, model, tokenizer, device, unique_filename, start_time):
    messages = []
    input_message = memory.create_message("user", prompt)
    messages.append(input_message)
    #print(messages)
    response = chat.generate_response(messages, model, tokenizer, device)  # Adjusted to use just the prompt
    #print(response)
    response = memory.preprocess_and_correct_json_string(response)
    print(response)
    
    response_message = memory.create_message("assistant", response)
    messages.append(response_message)
    
    # Save conversation to unique file for this thread
    memory.save_message(messages, unique_filename)
    response_time = timing() - start_time
    print(f"Response Time: {response_time:.2f} seconds")

def main():
    models = {}
    tokenizers = {}
    devices = {}

    models, tokenizers, devices = initial_models()
        
    base_filename = 'memories/dev'
    
    while True:
        prompt = input(">")
        if prompt.lower() == 'exit':
            break
        
        start_time = timing()
        
        prompts = [prompt,f"You are a subprocess for an artificial intelligence, that only comunicates using JSON. You act as my subconscious and are a preprocessor that serves to help me better understand a prompt and my improve responses. You are tasked with identifying the key components of a prompt. \nThe expected output from you has to be:\n\t\{{\n\t\t\"\"key_components\"\": [\"list of key components identified in the prompt\"],\n\t\t\"\"prompt_type\"\": \"Type of prompt, use multiple if needed (e.g.,question, request for explanation, task)\",\n\t\t\"\"response_type\"\":\"Appropriate response format (e.g., explanation, list, detailed answer, python code, simple answer)\",\n\t\t\"\"notes\"\": \"Any initial observations that might guide research or response structure\"\n\t\}}\nOnly respond with in JSON. I have recieved the following prompt, identify the key components of the prompt: \"{prompt}\""]
        
        threads = []
        
        for idx, (p, d) in enumerate(zip(prompts, devices)): # Change implementation for more than 2 GPUs
            unique_filename = f"{base_filename}_{idx}.json"  # Create a unique filename for each thread
            thread = threading.Thread(target=generate_and_print_response, args=(p, models[d], tokenizers[d], d, unique_filename, start_time))
            threads.append(thread)
            thread.start()
            # thread.join()  # Optional, wait for the thread to complete. Remove for asynchronous.
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()


if __name__ == "__main__":
    main()
