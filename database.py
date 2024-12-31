import mysql.connector
import config

# Function to load user by email
def load_user_by_email(email):
    """Select user from the database by email."""
    conn = get_database_connection()
    create_user_table()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT id, email, password
        FROM users
        WHERE email = %(email)s;""", {'email': email})
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result  # This will now return a dictionary with 'id', 'email', and 'password'

# Function to add user to the database
def add_user(email, password):
    """Add a user to the database."""
    conn = get_database_connection()
    create_user_table()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""INSERT INTO users (email, password)
                      VALUES (%s, %s);""", (email, password))  # For simplicity, storing password in plain text (use hashing in production)
    conn.commit()
    cursor.close()
    conn.close()

# Function to get database connection
def get_database_connection():
    """Build a database connection."""
    conn = mysql.connector.connect(user=config.DATABASE_USER, password=config.DATABASE_PASSWORD,
                                   host=config.DATABASE_HOST,
                                   database=config.DATABASE_DB_NAME,
                                   ssl_disabled=True)  # see https://bugs.mysql.com/90585
    return conn

# Function to create table if it doesn't exist
def create_user_table():
    """Creates user table if it does not already exist."""
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

