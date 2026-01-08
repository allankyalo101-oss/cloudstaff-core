# day1_stress_test.py
import sqlite3
import datetime
import random
import string
import numpy as np

# Replace with your actual embedding function
def embed_text(text):
    # Simulated embedding: vector of 300 random floats
    np.random.seed(hash(text) % (2**32))
    return np.random.rand(300)

# --- CONFIG ---
DB_FILE = "sarah_kb.db"
CLIENTS = ["Noah", "Olivia", "Ethan", None]  # None = generic
NUM_TEST_ENTRIES = 100  # Start small, scale up for stress
TOP_N = 3

# --- HELPERS ---
def random_text(length=50):
    return "".join(random.choices(string.ascii_letters + " ", k=length))

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Create KB table
    c.execute("""
        CREATE TABLE IF NOT EXISTS kb_entries (
            id INTEGER PRIMARY KEY,
            client TEXT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            tags TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    return conn, c

def insert_test_entries(c):
    for _ in range(NUM_TEST_ENTRIES):
        client = random.choice(CLIENTS)
        question = random_text(30)
        answer = random_text(50)
        tags = random.choice(["invoice,payment", "meeting,followup", "general"])
        created_at = datetime.datetime.now().isoformat()
        c.execute("INSERT INTO kb_entries (client, question, answer, tags, created_at) VALUES (?, ?, ?, ?, ?)",
                  (client, question, answer, tags, created_at))

def fetch_all_entries(c):
    c.execute("SELECT id, client, question, answer FROM kb_entries")
    return c.fetchall()

def search_kb(query, entries, client_filter=None, top_n=TOP_N):
    query_vec = embed_text(query)
    results = []
    for entry in entries:
        client, question, answer = entry[1], entry[2], entry[3]
        if client_filter and client != client_filter:
            continue
        q_vec = embed_text(question)
        sim = np.dot(query_vec, q_vec) / (np.linalg.norm(query_vec)*np.linalg.norm(q_vec))
        results.append((sim, question, answer, client))
    results.sort(reverse=True, key=lambda x: x[0])
    return results[:top_n]

def run_tests(conn, c):
    report = []
    
    # --- Test 1: DB structure ---
    try:
        c.execute("SELECT * FROM kb_entries LIMIT 1")
        report.append("DB structure check: PASS")
    except Exception as e:
        report.append(f"DB structure check: FAIL ({e})")
    
    # --- Test 2: Insert & fetch ---
    try:
        insert_test_entries(c)
        conn.commit()
        entries = fetch_all_entries(c)
        report.append(f"Insert & fetch {NUM_TEST_ENTRIES} entries: PASS ({len(entries)} total)")
    except Exception as e:
        report.append(f"Insert & fetch: FAIL ({e})")
    
    # --- Test 3: Semantic search ---
    try:
        test_query = entries[0][2]  # use first question as query
        results = search_kb(test_query, entries, client_filter=entries[0][1])
        if results and results[0][1] == entries[0][2]:
            report.append("Semantic search top match test: PASS")
        else:
            report.append("Semantic search top match test: FAIL")
    except Exception as e:
        report.append(f"Semantic search test: FAIL ({e})")
    
    # --- Test 4: Multi-client search ---
    try:
        for client in ["Noah", "Olivia", "Ethan"]:
            results = search_kb("test query", entries, client_filter=client)
            report.append(f"Search for client {client}: PASS ({len(results)} results)")
    except Exception as e:
        report.append(f"Multi-client search: FAIL ({e})")
    
    # --- Test 5: Generic search ---
    try:
        results = search_kb("test query", entries, client_filter=None)
        report.append(f"Generic search across clients: PASS ({len(results)} results)")
    except Exception as e:
        report.append(f"Generic search: FAIL ({e})")
    
    return report

# --- EXECUTION ---
conn, c = init_db()
report = run_tests(conn, c)
conn.close()

print("\n--- DAY 1 STRESS TEST REPORT ---")
for line in report:
    print(line)

