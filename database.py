import sqlite3


def create_table_history():
    db = sqlite3.connect('audiodown.db')
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id BIGINT,
        link TEXT
    );
    ''')

    db.commit()
    db.close()


# create_table_history()


def save_history(*args):
    db = sqlite3.connect('audiodown.db')
    cursor = db.cursor()
    cursor.execute('''
    INSERT INTO history(chat_id, link)
    VALUES(?, ?)
    ''', args)
    db.commit()
    db.close()


def get_history(chat_id):
    db = sqlite3.connect('audiodown.db')
    cursor = db.cursor()
    cursor.execute('''
    SELECT link FROM history
    WHERE chat_id = ? ORDER BY history_id DESC LIMIT 5
    ''', (chat_id,))
    history = cursor.fetchall()
    db.close()
    return history


def create_table_users():
    db = sqlite3.connect('audiodown.db')
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id BIGINT,
        full_name VARCHAR(150),
        phone TEXT
    );
    ''')
    db.commit()
    db.close()


# create_table_users()

def save_user_data(*args):
    db = sqlite3.connect('audiodown.db')
    cursor = db.cursor()
    cursor.execute('''
    INSERT INTO users(chat_id, full_name, phone)
    VALUES(?, ?, ?)
    ''', args)
    db.commit()
    db.close()


def get_user(chat_id):
    db = sqlite3.connect('audiodown.db')
    cursor = db.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE chat_id=?
    ''', (chat_id,))
    user = cursor.fetchone()
    db.close()
    return user
