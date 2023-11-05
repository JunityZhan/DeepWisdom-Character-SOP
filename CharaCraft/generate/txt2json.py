import argparse
import os
import glob
import json


def split_dialogue(line):
    if "：" in line:
        return line.split("：", 1)
    elif ": " in line:
        return line.split(": ", 1)
    else:
        return "", line


def process_text_file(file_path, name):
    # 读取文本文件
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 将文本分割成对话列表
    dialogues = text.split('\n')

    # 解析对话并构建JSON结构
    history = []
    instruction = ""
    output = ""
    for i in range(len(dialogues) - 1):
        speaker, content = split_dialogue(dialogues[i])
        next_speaker, next_content = split_dialogue(dialogues[i + 1])

        # 如果下一个说话者是指定的角色，则保存当前的对话内容到history的提问中，并设置instruction
        if next_speaker == name:
            history.append([content, ""])
            instruction = content

        # 如果当前说话者是指定的角色，则保存其对话内容到history的回答中，并更新output
        if speaker == name:
            if history and history[-1][1] == "":
                history[-1][1] = content
            output = content

    # 移除history中回答为空的项
    history = [item for item in history if item[1] != ""]

    # 如果output为空，尝试从history中找到一个非空回答
    if output == "" and history:
        output = history[-1][1]

    # 构建JSON结构
    json_output = {
        "instruction": instruction,
        "input": "",
        "output": output,
        "history": history[:-1] if history else []  # 移除最后一个对话，如果存在的话
    }

    return json_output


def main():
    parser = argparse.ArgumentParser(description='Process text files and generate JSON output.')
    parser.add_argument('--name', type=str, required=True, help='The specified role name')
    args = parser.parse_args()

    # 获取指定角色名
    name = args.name

    # 获取当前工作目录
    cwd = os.getcwd()

    # 查找所有txt文件
    txt_files = glob.glob(os.path.join(cwd, 'text', name, '*.txt'))

    # 处理每个文本文件并生成JSON输出
    result = []
    for txt_file in txt_files:
        json_output = process_text_file(txt_file, name)
        result.append(json_output)

    # 将结果保存到JSON文件
    output_file = os.path.join(cwd, 'text', name, 'result.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f'Results saved to {output_file}')


if __name__ == '__main__':
    main()
