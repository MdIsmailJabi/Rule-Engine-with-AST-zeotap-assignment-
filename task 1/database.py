
import sqlite3

def initialize_db():
    conn = sqlite3.connect("rules.db")
    cursor = conn.cursor()

    # Create table for storing rules
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_string TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def store_rule(rule_string):
    conn = sqlite3.connect("rules.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rules (rule_string) VALUES (?)", (rule_string,))
    conn.commit()
    conn.close()

def get_rules():
    conn = sqlite3.connect("rules.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rule_string FROM rules")
    rules = cursor.fetchall()
    conn.close()
    return [rule[0] for rule in rules]
