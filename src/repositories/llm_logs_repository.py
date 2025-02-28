import datetime
from src.repositories.db_manager import DBManager


class LLMLogsRepository:
    db_manager: DBManager

    def __init__(self):
        self.db_manager = DBManager()

    def cache_response(self, prompt_hash: str, prompt: str, response: str):
        query = """
        INSERT INTO llm_logs (prompt_hash, prompt, response, timestamp)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(prompt_hash) DO UPDATE SET response = excluded.response, timestamp = excluded.timestamp;
        """
        self.db_manager.execute_query(query, (prompt_hash, prompt, response, datetime.datetime.now().isoformat()))

    def get_cached_response(self, prompt_hash: str):
        query = "SELECT response FROM llm_logs WHERE prompt_hash = ? LIMIT 1"
        result = self.db_manager.execute_query(query, (prompt_hash,), fetchone=True)
        return result[0] if result else None

    def clear_cache(self):
        query = "DELETE FROM llm_logs"
        self.db_manager.execute_query(query)
