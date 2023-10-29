import sys
import os
import argparse
import gradio as gr

current_script_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_script_path)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from chatharuhi import ChatHaruhi

def main(role_name, name):
    db_folder = os.path.join('text', role_name)
    prompt_path = os.path.join('prompt', 'default.txt')

    with open(prompt_path, 'r', encoding='utf8') as f:
        system_prompt = f.read().replace('{role_name}', role_name).replace('character', name)

    chatbot = ChatHaruhi(
        system_prompt=system_prompt,
        llm='openai',
        story_text_folder=db_folder,
        max_len_story=1000,
        role_name=role_name
    )

    def respond(message, history):
        chatbot.dialogue_history = [tuple(dialogue) for dialogue in history]
        print(chatbot.dialogue_history)
        print(chatbot.llm.print_prompt())
        return chatbot.chat(text=message, role=name)

    with gr.Blocks() as demo:
        gr.ChatInterface(fn=respond, examples=["Nice to meet you."], title="CharaCraft")
    demo.launch(debug=True, share=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a chatbot with Gradio interface.')
    parser.add_argument('--prompt', default='default', type=str, help='prompt of the role(should be in the prompt folder, give the name of the file')
    parser.add_argument('--role_name', type=str, help='Name of the role')
    parser.add_argument('--name', type=str, help='Name of you')
    args = parser.parse_args()
    main(args.role_name, args.name)
