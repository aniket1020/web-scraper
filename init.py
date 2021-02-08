import sqlite3

def init_db():
    db = sqlite3.connect('jobs.db')
    with open('schema.sql','r') as f:
        db.cursor().executescript(f.read())
    db.commit()

if __name__ == '__main__':
    init_db()