from src.repositories.repository import Repository
import datetime

class LLMLogsRepository(Repository):
    def table_name(self) -> str:
        return "llm_logs"

    def cache_response(self, run_id: str, prompt_hash: str, prompt: str, response: str):
        """
        Stores or updates an LLM response in the cache.
        """
        data = {
            "run_id": run_id,
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
        return result[4] if result else None

    def clear_cache(self):
        """
        Clears all cached LLM responses.
        """
        self.delete("1 = 1", ())

    def get_logs_by_run_id(self, run_id):
        records = self.fetch_all("run_id = ?", (run_id,))
        return [
            {
                "id": record[0],
                "run_id": record[1],
                "prompt_hash": record[2],
                "prompt": record[3],
                "response": record[4],
                "timestamp": record[5]
            }
            for record in records
        ] if records else None
