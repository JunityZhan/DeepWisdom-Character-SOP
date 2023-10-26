import torch
from transformers import BertTokenizer, BertModel
from scipy.spatial.distance import cosine
import jieba
import re
from sentence_transformers import SentenceTransformer, util
import jieba.analyse

class SimilarityFinder:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
        self.model = BertModel.from_pretrained("bert-base-chinese")
        self.sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def get_embedding_sbert(self, text):
        """使用SBERT获取文本的向量表示"""
        return self.sbert_model.encode(text, convert_to_numpy=True)

    def calculate_similarity_sbert(self, text1, text2):
        """计算两个文本的cosine相似度"""
        embedding1 = self.get_embedding_sbert(text1)
        embedding2 = self.get_embedding_sbert(text2)
        return 1 - cosine(embedding1, embedding2)

    def get_key_sentences(self, text, topK=5):
        """提取文本中的关键词或短语"""
        return jieba.analyse.extract_tags(text, topK=topK, withWeight=False)

    @staticmethod
    def length_penalty(sentence):
        """根据句子长度调整得分"""
        length = len(sentence.split())
        min_len, max_len = 5, 20
        if length < min_len:
            return 0.5
        elif length > max_len:
            return 1.5
        else:
            return 1

    def find_top_n_similar_contexts(self, sentence, paragraph, n=3):
        """使用关键词方法从按行分割的文段中找到与给定句子相似度排名前n的句子及其后一句"""

        lines = paragraph.split('\n')
        lines = [line.strip() for line in lines if len(line.strip()) > 0]

        keywords = self.get_key_sentences(sentence)

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

    with open('神里绫华Kamisato Ayaka.txt', 'r', encoding='utf-8') as f:
        paragraph = f.read()

    similar_sentence = ''
    user_input = input("请输入您的问题：")
    n = int(input("您希望获得前几个最相关的句子？"))

    top_n_results = finder.find_top_n_similar_contexts(user_input, paragraph, n)
    for idx, (context, similarity) in enumerate(top_n_results, 1):
        similar_sentence += context + '\n'
        print(f"和“{user_input}”第{idx}个最相关的文本内容是：\n\n{context}\n\n相似度为: {similarity:.4f}\n{'-'*40}")
    print("similar sentence:", similar_sentence)
=======
import torch
from transformers import BertTokenizer, BertModel
from scipy.spatial.distance import cosine
import jieba
import re
from sentence_transformers import SentenceTransformer, util
import jieba.analyse

class SimilarityFinder:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
        self.model = BertModel.from_pretrained("bert-base-chinese")
        self.sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def get_embedding_sbert(self, text):
        """使用SBERT获取文本的向量表示"""
        return self.sbert_model.encode(text, convert_to_numpy=True)

    def calculate_similarity_sbert(self, text1, text2):
        """计算两个文本的cosine相似度"""
        embedding1 = self.get_embedding_sbert(text1)
        embedding2 = self.get_embedding_sbert(text2)
        return 1 - cosine(embedding1, embedding2)

    def get_key_sentences(self, text, topK=5):
        """提取文本中的关键词或短语"""
        return jieba.analyse.extract_tags(text, topK=topK, withWeight=False)

    @staticmethod
    def length_penalty(sentence):
        """根据句子长度调整得分"""
        length = len(sentence.split())
        min_len, max_len = 5, 20
        if length < min_len:
            return 0.5
        elif length > max_len:
            return 1.5
        else:
            return 1

    def find_top_n_similar_contexts(self, sentence, paragraph, n=3):
        """使用关键词方法从按行分割的文段中找到与给定句子相似度排名前n的句子及其后一句"""

        lines = paragraph.split('\n')
        lines = [line.strip() for line in lines if len(line.strip()) > 0]

        keywords = self.get_key_sentences(sentence)

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

    with open('神里绫华Kamisato Ayaka.txt', 'r', encoding='utf-8') as f:
        paragraph = f.read()

    similar_sentence = ''
    user_input = input("请输入您的问题：")
    n = int(input("您希望获得前几个最相关的句子？"))

    top_n_results = finder.find_top_n_similar_contexts(user_input, paragraph, n)
    for idx, (context, similarity) in enumerate(top_n_results, 1):
        similar_sentence += context + '\n'
        print(f"和“{user_input}”第{idx}个最相关的文本内容是：\n\n{context}\n\n相似度为: {similarity:.4f}\n{'-'*40}")
    print("similar sentence:", similar_sentence)
>>>>>>> d596178cf38d24cae214f3bf53055b417653cca8
