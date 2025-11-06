import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "site.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_conn():
    return sqlite3.connect(DB_PATH)

def apply_schema(schema):
    conn = get_conn()
    cur = conn.cursor()
    for table in schema.get("tables", []):
        cols = ", ".join([f"{c['name']} {c['type']}" for c in table["columns"]])
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table['name']} ({cols});")
    conn.commit()
    conn.close()
