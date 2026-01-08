import sqlite3
import os
import numpy as np
from openai import OpenAI

# Setup OpenAI client
client = OpenAI(api_key="YOUR_OPENAI_KEY")  # Replace with your key

# KB DB path
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/sarah_kb.db')

# Generate embeddings
def embed_text(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

# Search KB by semantic similarity
def search_kb(query: str, client_filter=None, top_n=3):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if client_filter:
        c.execute('SELECT id, question, answer FROM kb_entries WHERE client=?', (client_filter,))
    else:
        c.execute('SELECT id, question, answer FROM kb_entries')
    
    rows = c.fetchall()
    conn.close()

    query_vec = embed_text(query)
    results = []
    
    for row in rows:
        id, q, a = row
        q_vec = embed_text(q)
        score = np.dot(query_vec, q_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(q_vec))
        results.append((score, a))
    
    results.sort(reverse=True, key=lambda x: x[0])
    return [a for _, a in results[:top_n]]

# Example usage
if __name__ == "__main__":
    answers = search_kb("How do I pay my invoice?", client_filter="Noah")
    print("Top KB answers:", answers)
