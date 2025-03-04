from src.repositories.repository import Repository

class ModelOutputsRepository(Repository):
    def table_name(self) -> str:
        return "model_outputs"

