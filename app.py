import pandas as pd
import time

import chat
import memory

def timing():
    current_time = time.time()
    return current_time

def main():
    
    messages, model, tokenizer, device = chat.initialize_chat()
    filename ='memories/dev.json'

    
    while True:
            try:
                # messages = memory.load_memory('tools/function_calling.json')
                messages = []
                prompt = input(">")
                
                start_time = timing()
                
                input_message = memory.create_message("user",prompt)

                messages.append(input_message)
                response = chat.generate_response(messages, model, tokenizer, device)
                
                response_message = memory.create_message("assistant",response)  
                messages.append(response_message)
                messages_df = pd.DataFrame(messages)
                print(messages_df)
                
                memory.save_message(messages,filename)
                print(response)
                
                response_time = timing()-start_time
                print(response_time)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
