import sqlite3

DATABASE = 'tasks.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db():
    with connect_db() as conn:
        with open('schema.sql', 'r') as f: #this was because the 2 sql files i made find out what does or put them together and then keep same
            conn.executescript(f.read())

def query_db(query, args=(), one=False):
    conn = connect_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    conn = connect_db()
    cur = conn.execute(query, args)
    conn.commit()
    conn.close()