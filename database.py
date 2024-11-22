import sqlite3

def init_db():
    try:
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            # Create users table if not exists
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            # Create user_inputs table to store prediction inputs
            c.execute('''
                CREATE TABLE IF NOT EXISTS user_inputs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    gender INTEGER,
                    age INTEGER,
                    hypertension INTEGER,
                    heart_disease INTEGER,
                    ever_married INTEGER,
                    work INTEGER,
                    residence INTEGER,
                    avg_glucose_level REAL,
                    bmi REAL,
                    smoking INTEGER,
                    prediction INTEGER,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            ''')
            conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")

def add_user(username, password):
    try:
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while adding a user: {e}")

def get_user(username):
    try:
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = c.fetchone()
            return user
    except sqlite3.Error as e:
        print(f"An error occurred while fetching the user: {e}")
        return None

def save_user_input(username, gender, age, hypertension, heart_disease, ever_married, work, residence,
                     avg_glucose_level, bmi, smoking, prediction):
    try:
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO user_inputs (username, gender, age, hypertension, heart_disease, ever_married,
                                         work, residence, avg_glucose_level, bmi, smoking, prediction)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, gender, age, hypertension, heart_disease, ever_married, work, residence, avg_glucose_level,
                  bmi, smoking, prediction))
            conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while saving user input: {e}")
