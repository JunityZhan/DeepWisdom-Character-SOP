from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from transformers_stream_generator.main import NewGenerationMixin, StreamGenerationConfig
import torch
import argparse
import json

lora_folder = ''
model_folder = ''
config = PeftConfig.from_pretrained(lora_folder,
                                    trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_folder,
                                              torch_dtype=torch.float16,
                                              device_map="auto",
                                              trust_remote_code=True)
model = PeftModel.from_pretrained(model,
                                  lora_folder,
                                   device_map="auto",
                                   torch_dtype=torch.float16,
                                   trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_folder,
                                          trust_remote_code=True)
history = []
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def respond(msg, temp, rep, max_len, top_p, top_k):
    msg = "旅行者: " + msg + "\n" + "神里绫华: "
    input_ids = tokenizer.encode(msg)
    input_ids = torch.LongTensor([input_ids]).to(device)
    generation_config = model.generation_config
    gen_kwargs = {}
    gen_kwargs.update(dict(
        input_ids=input_ids,
        temperature=float(temp),
        top_p=float(top_p),
        top_k=top_k,
        repetition_penalty=float(rep),
        max_new_tokens=max_len,
        do_sample=True,
    ))
    ret = model.generate(**gen_kwargs)
    ret = tokenizer.decode(ret[0])
    return ret


def evaluate_sample(sample, temp, rep, max_len, top_p, top_k):
    generated_response = respond(sample["query"], temp, rep, max_len, top_p, top_k)
    score = 0
    for keyword in sample["keywords"]:
        if keyword in generated_response:
            score += 1
    return score, generated_response

def main(args):
    # 载入测试集
    with open(args.testset_json, 'r') as f:
        testset = json.load(f)

    total_score = 0
    for sample in testset:
        score, _ = evaluate_sample(sample, args.temp, args.rep, args.max_len, args.top_p, args.top_k)
        total_score += score

    print(f"Total Score: {total_score}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a language model based on keyword hits.")
    parser.add_argument("--testset", type=str, help="Path to the testset JSON file.")
    parser.add_argument("--lora_folder", type=str, default="", help="Path to the LORA folder.")
    parser.add_argument("--model_folder", type=str, default="", help="Path to the model folder.")
    parser.add_argument("--temp", type=float, default=0, help="Temperature for generation.")
    parser.add_argument("--rep", type=float, default=1.0, help="Repetition penalty for generation.")
    parser.add_argument("--max_len", type=int, default=50, help="Maximum length for generation.")
    parser.add_argument("--top_p", type=float, default=0.9, help="Top-p for nucleus sampling.")
    parser.add_argument("--top_k", type=int, default=50, help="Top-k for sampling.")

    args = parser.parse_args()
    main(args)
