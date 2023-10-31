import os
import json
import argparse


class DialogueParser:
    def __init__(self, name, folder_path):
        self.name = name
        self.folder_path = folder_path

    def parse_dialogues(self):
        results = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(self.folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    dialogues, current_dialogue = [], []
                    instruction, speaker = "", ""

                    for line in lines:
                        line = line.strip()
                        if line:
                            if "：" in line:
                                speaker, content = line.split("：", 1)
                                content = content.strip()
                                if speaker == self.name:
                                    if instruction:
                                        current_dialogue.append((instruction, content))
                                        instruction = ""
                                    else:
                                        current_dialogue.append(("", content))
                                else:
                                    instruction = content
                            elif current_dialogue:
                                _, last_content = current_dialogue[-1]
                                current_dialogue[-1] = ("", last_content + " " + line)

                    if current_dialogue:
                        dialogues.append(current_dialogue)

                for dialogue in dialogues:
                    result = {"instruction": "", "input": "", "output": "", "history": []}
                    if len(dialogue) > 1:
                        result["history"] = [[instruction, output] for instruction, output in dialogue[:-1]]
                    if dialogue:
                        result["instruction"], result["output"] = dialogue[-1]
                    results.append(result)

        return results

    def save_to_json(self, results):
        output_file = f"output_{self.name}.json"
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
            print(f"Results have been written to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Parse dialogues from txt files to json.')
    parser.add_argument('--name', required=True, help='The name to parse from dialogues')
    args = parser.parse_args()

    folder_path = os.path.join("./text", args.name)
    dialogue_parser = DialogueParser(args.name, folder_path)
    results = dialogue_parser.parse_dialogues()
    dialogue_parser.save_to_json(results)


if __name__ == "__main__":
    main()
