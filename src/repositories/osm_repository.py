from src.repositories.repository import Repository
import datetime

class OSMRepository(Repository):
    def table_name(self) -> str:
        return "osm_cache"

    def cache_response(self, query_hash: str, response: str):
        """
        Caches OpenStreetMap query results.
        """
        data = {
            "query_hash": query_hash,
            "response": response,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.insert(data)

    def get_cached_response(self, query_hash: str):
        """
        Retrieves a cached response by query hash.
        """
        result = self.fetch_one("query_hash = ?", (query_hash,))
        return result[2] if result else None

    def clear_cache(self):
        """
        Clears all cached OSM responses.
        """
        self.delete("1 = 1", ())
