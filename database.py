import sqlite3

# Function to create the SQLite database and table
def create_database():
    conn = sqlite3.connect("weather_app.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_responses (
            id INTEGER PRIMARY KEY,
            user_input TEXT,
            response_text TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to insert user input and response into the database
def insert_response(user_input, response_text):
    conn = sqlite3.connect("weather_app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_responses (user_input, response_text) VALUES (?, ?)", (user_input, response_text))
    conn.commit()
    conn.close()

# Function to retrieve all user responses from the database
def get_all_responses():
    conn = sqlite3.connect("weather_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_input, response_text FROM user_responses")
    responses = cursor.fetchall()
    conn.close()
    return responses
