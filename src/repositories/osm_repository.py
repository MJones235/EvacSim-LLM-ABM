from src.repositories.db_manager import DBManager


class OSMRepository:
    db_manager: DBManager

    def __init__(self):
        self.db_manager = DBManager()

    def cache_response(self, query_hash: str, response: str):
        query = """
        INSERT INTO osm_cache (query_hash, response, timestamp)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(query_hash) DO UPDATE SET response = excluded.response, timestamp = excluded.timestamp;
        """
        self.db_manager.execute_query(query, (query_hash, response))

    def get_cached_response(self, query_hash: str):
        query = "SELECT response FROM osm_cache WHERE query_hash = ? LIMIT 1"
        result = self.db_manager.execute_query(query, (query_hash,), fetchone=True)
        return result[0] if result else None

    def clear_cache(self):
        query = "DELETE FROM osm_cache"
        self.db_manager.execute_query(query)
