from pathlib import Path
import sqlite3

# -------------------------------------------------
# Database Configuration
# -------------------------------------------------

DATABASE_FOLDER = Path("data")
DATABASE_FOLDER.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_FOLDER / "unbubble.db"


# -------------------------------------------------
# Database Connection
# -------------------------------------------------

def get_connection():
    """
    Returns a SQLite connection.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------------------------------
# Database Initialization
# -------------------------------------------------

def initialize_database():
    """
    Creates all required tables.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------------
    # Opportunities
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT NOT NULL,

        organizer TEXT,

        category TEXT,

        description TEXT,

        website TEXT,

        deadline DATE,

        status TEXT,

        priority TEXT,

        funding_amount TEXT,

        location TEXT,

        notes TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -------------------------------
    # Tasks
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        opportunity_id INTEGER,

        task_name TEXT,

        assigned_to TEXT,

        due_date DATE,

        status TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # -------------------------------
    # Team Members
    # -------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS team_members(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT,

        role TEXT
    )
    """)

    conn.commit()
    conn.close()