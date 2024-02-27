import keyboard
import threading
import ollama

CYAN = "\033[36m"
RESET_COLOR = "\033[0m"

def chat(prompt, system):
    response = ollama.chat(model='gemma:2b-instruct', messages=[
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': prompt},
    ])
    print(response['message']['content'])
    return response['message']['content']

prompt = ""
last_preview = ""

def open_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def update_preview(prompt, system):
    global last_preview
    if len(prompt) >= 14:
        last_preview = chat(prompt, system)
        with open("last_preview.txt", "w") as f:
            f.write(last_preview)

def capture_input(system_message):
    global prompt
    space_count = 0
    
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            
            if key == 'backspace':
                if prompt:
                    prompt = prompt[:-1]
                    if prompt.endswith(" "):
                        space_count = max(0, space_count - 1)
                    print(f"\b \b", end="", flush=True)
            elif key == "space":
                prompt += " "
                print(f"{CYAN} {RESET_COLOR}", end="", flush=True)
                space_count += 1
                if space_count > 3:
                    threading.Thread(target=update_preview, args=(prompt, system_message,), daemon=True).start()
                print(" ", end="", flush=True)
            elif len(key) == 1:
                prompt += key
                print(f"{CYAN}{key}{RESET_COLOR}", end="", flush=True)
            elif key == 'esc':  # Exit condition
                break
            else:
                continue

if __name__ == "__main__":
    system_message = open_file("chatbot1.txt")
    capture_input(system_message)
