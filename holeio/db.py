import sqlite3

def create_tables():
  db = sqlite3.connect('holeio.db')
  with db:
    db.execute('''create table if not exists history (message text, timestamp text DEFAULT CURRENT_TIMESTAMP) ''')
create_tables()

def add_history(message):
  db = sqlite3.connect('holeio.db')
  with db:
    db.execute('''insert into history (message) values (?)''', (message, ))

def get_history(limit=1000, offset=0):
  db = sqlite3.connect('holeio.db')
  with db:
    return db.execute('''select datetime(timestamp, 'localtime'), message from history ORDER BY timestamp DESC LIMIT ? OFFSET ?''',
                      (limit, offset)).fetchall()

def clear_history():
  db = sqlite3.connect('holeio.db')
  with db:
    db.execute('''delete from history''')
