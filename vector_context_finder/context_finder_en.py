import torch
from transformers import BertTokenizer, BertModel
from scipy.spatial.distance import cosine
from sentence_transformers import SentenceTransformer, util

class SimilarityFinder:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")  # Use English BERT model
        self.model = BertModel.from_pretrained("bert-base-uncased")  # Use English BERT model
        self.sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # This model supports English

    def get_embedding_sbert(self, text):
        return self.sbert_model.encode(text, convert_to_numpy=True)

    def calculate_similarity_sbert(self, text1, text2):
        embedding1 = self.get_embedding_sbert(text1)
        embedding2 = self.get_embedding_sbert(text2)
        return 1 - cosine(embedding1, embedding2)

    # Removed the jieba keyword extraction method, you might want to use another method or library for English keyword extraction

    @staticmethod
    def length_penalty(sentence):
        length = len(sentence.split())
        min_len, max_len = 5, 20
        if length < min_len:
            return 0.5
        elif length > max_len:
            return 1.5
        else:
            return 1

    def find_top_n_similar_contexts(self, sentence, paragraph, n=3):
        lines = paragraph.split('\n')
        lines = [line.strip() for line in lines if len(line.strip()) > 0]

        # For simplicity, consider the user input as the keyword for English
        keywords = [sentence]

        scores = {idx: 0 for idx, _ in enumerate(lines)}
        for keyword in keywords:
            for idx, line in enumerate(lines):
                if keyword in line:
                    scores[idx] += 10
                similarity = self.calculate_similarity_sbert(keyword, line) * self.length_penalty(line)
                scores[idx] += similarity

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        top_n_contexts = []
        for idx, score in sorted_scores[:n]:
            context = [lines[idx]]
            if idx + 1 < len(lines):
                context.append(lines[idx + 1])
            top_n_contexts.append(("\n".join(context), score))

        return top_n_contexts

if __name__ == "__main__":
    finder = SimilarityFinder()

    with open('english_text.txt', 'r', encoding='utf-8') as f:
        paragraph = f.read()

    similar_sentence = ''
    user_input = input("Please enter your question:")
    n = int(input("How many top relevant sentences would you like to retrieve?"))

    top_n_results = finder.find_top_n_similar_contexts(user_input, paragraph, n)
    for idx, (context, similarity) in enumerate(top_n_results, 1):
        similar_sentence += context + '\n'
        print(f"The {idx}th most relevant text to '{user_input}' is:\n\n{context}\n\nSimilarity: {similarity:.4f}\n{'-'*40}")
    print("Similar sentence:", similar_sentence)
