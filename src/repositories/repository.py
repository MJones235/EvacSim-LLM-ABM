from abc import ABC, abstractmethod

from src.repositories.db_manager import DBManager

class Repository(ABC):
    db_manager: DBManager

    def __init__(self):
        self.db_manager = DBManager()

    @abstractmethod
    def table_name(self) -> str:
        pass

    def insert(self, data: dict):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {self.table_name()} ({columns}) VALUES ({placeholders})"
        self.db_manager.execute_query(query, tuple(data.values()))

    def fetch_one(self, condition: str, params: tuple):
        query = f"SELECT * FROM {self.table_name()} WHERE {condition} LIMIT 1"
        return self.db_manager.execute_query(query, params, fetchone=True)

    def fetch_all(self, condition: str = None, params: tuple = ()):
        query = f"SELECT * FROM {self.table_name()}"
        if condition:
            query += f" WHERE {condition}"
        return self.db_manager.execute_query(query, params, fetchall=True)

    def delete(self, condition: str, params: tuple):
        query = f"DELETE FROM {self.table_name()} WHERE {condition}"
        self.db_manager.execute_query(query, params)
