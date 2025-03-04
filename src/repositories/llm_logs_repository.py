from src.repositories.repository import Repository
import datetime

class LLMLogsRepository(Repository):
    def table_name(self) -> str:
        return "llm_logs"

    def cache_response(self, prompt_hash: str, prompt: str, response: str):
        """
        Stores or updates an LLM response in the cache.
        """
        data = {
            "prompt_hash": prompt_hash,
            "prompt": prompt,
            "response": response,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.insert(data)

    def get_cached_response(self, prompt_hash: str):
        """
        Retrieves a cached response by prompt hash.
        """
        result = self.fetch_one("prompt_hash = ?", (prompt_hash,))
        return result[2] if result else None

    def clear_cache(self):
        """
        Clears all cached LLM responses.
        """
        self.delete("1 = 1", ())
