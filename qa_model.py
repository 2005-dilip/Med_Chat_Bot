# qa_model.py

import csv
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from langchain.prompts import PromptTemplate

# Load CSV Data
def load_csv_data(csv_file):
    data = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row["Chunk Text"]
            embedding = list(map(float, row["Embedding"].split(',')))
            data.append({"text": text, "embedding": embedding})
    return data


# Simple retriever to find the best matching text chunk
def retrieve_from_csv(data, query_embedding, top_k=2):
    scores = []
    for item in data:
        if len(query_embedding) != len(item['embedding']):
            continue
        score = np.dot(query_embedding, item['embedding']) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(item['embedding']))
        scores.append((score, item['text']))
    scores.sort(reverse=True, key=lambda x: x[0])
    return [text for _, text in scores[:top_k]]


# Embeddings class using SentenceTransformer
class Embeddings:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Choose an appropriate model

    def embed_query(self, query):
        return self.model.encode(query).tolist()


# Initialize embeddings model and load CSV data
embeddings = Embeddings()
csv_data = load_csv_data("output.csv")

# LLM model and prompt setup
prompt_template = """
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

# Switch to Hugging Face's pipeline for DistilGPT-2
llm = pipeline('text-generation', model='distilgpt2')


# QA chain setup
def qa_chain(query):
    query_embedding = embeddings.embed_query(query)
    retrieved_texts = retrieve_from_csv(csv_data, query_embedding, top_k=2)
    context = " ".join(retrieved_texts)

    # Generate response from the LLM
    result = llm(f"Context: {context}\nQuestion: {query}", max_length=450, num_return_sequences=1)

    # Access the generated text
    generated_text = result[0]['generated_text']

    return generated_text
