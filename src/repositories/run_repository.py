from src.repositories.repository import Repository

class RunRepository(Repository):
    def table_name(self) -> str:
        return "runs"

    def store_run_metadata(self, metadata: dict):
        """
        Inserts a new simulation run entry.
        """
        self.insert(metadata)

    def fetch_run_metadata(self, run_id: str):
        """
        Retrieves metadata for a specific run.
        """
        return self.fetch_one("run_id = ?", (run_id,))

    def fetch_all_runs(self):
        """
        Retrieves metadata for all runs.
        """
        return self.fetch_all()

    def delete_run(self, run_id: str):
        """
        Deletes a run entry.
        """
        self.delete("run_id = ?", (run_id,))
