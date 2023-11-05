import json
import sys
import os
import argparse
import gradio as gr

current_script_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_script_path)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from chatharuhi import ChatHaruhi

def main(prompt, role_name, name, file):
    db_folder = os.path.join('text', role_name)
    prompt_path = os.path.join('prompt', prompt+'.txt')
    json_path = os.path.join('text', file+'.json')
    with open(prompt_path, 'r', encoding='utf8') as f:
        system_prompt = f.read().replace('{role_name}', role_name).replace('character', name)

    chatbot = ChatHaruhi(
        system_prompt=system_prompt,
        llm='openai',
        story_text_folder=db_folder,
        max_len_story=4000,
        role_name=role_name
    )
    # load json file, iterate the list, each element is a dict, and key is text.
    with open(json_path, 'r', encoding='utf8') as f:
        json_list = json.load(f)
    new_json = []
    for json_dict in json_list:

        # 运行chatbot，结果写入新的json文件，格式为
        # {
        #    "instruction": json_dict['text'],
        #    "input": "",
        #   "output": chatbot.chat(text=json_dict['text'], role=name)
        #    "history": []
        # }
        new_json.append({
            "instruction": json_dict['text'],
            "input": "",
            "output": chatbot.chat(text=json_dict['text'], role=name),
            "history": []
        })
        # 先写入txt备份
        with open('text/backup.txt', 'a', encoding='utf8') as f:
            f.write(new_json[-1]['output']+'\n')
            f.write('=====\n')
        # 再写入json
    with open(f'text/{role_name}.json', 'a', encoding='utf8') as f:
        json.dump(new_json, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a chatbot with Gradio interface.')
    parser.add_argument('--prompt', default='default', type=str, help='prompt of the role(should be in the prompt folder, give the name of the file')
    parser.add_argument('--role_name', type=str, help='Name of the role')
    parser.add_argument('--name', type=str, help='Name of you')
    parser.add_argument('--file', type=str, help='Name of file')
    args = parser.parse_args()
    main(args.prompt, args.role_name, args.name, args.file)
