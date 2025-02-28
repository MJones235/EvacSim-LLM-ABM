import logging
import sqlite3

class DBManager:
    db_path = "outputs.sqlite"
    
    def __init__(self):
        self._connect().execute("PRAGMA foreign_keys = ON;")
        self._initialise_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path, check_same_thread=False)
    
    def _initialise_db(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.executescript(self._schema())
            conn.commit()

    def execute_query(self, query, params=(), fetchone=False, fetchall=False):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                if fetchone:
                    return cursor.fetchone()
                if fetchall:
                    return cursor.fetchall()
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return None        

    def _schema(self):
        return """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            time TEXT,
            simulation_time TEXT,
            address TEXT,
            simulation_radius REAL,
            n_agents INTEGER
        );

        CREATE TABLE IF NOT EXISTS population (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT,
            name TEXT,
            age INTEGER,
            occupation TEXT,
            current_location TEXT,
            leave_time TEXT,
            plans TEXT,
            FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS llm_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT,
            prompt_hash TEXT UNIQUE,
            prompt TEXT,
            response TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE CASCADE
        );
        """

    
        