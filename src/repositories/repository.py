from abc import ABC, abstractmethod
from src.repositories.db_manager import DBManager

class Repository(ABC):
    """
    Abstract repository class providing common database operations.
    """
    def __init__(self):
        self.db_manager = DBManager()

    @abstractmethod
    def table_name(self) -> str:
        """
        Subclasses must define the table name.
        """
        pass

    def insert(self, data: dict):
        """
        Inserts a record into the table.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {self.table_name()} ({columns}) VALUES ({placeholders})"
        self.db_manager.execute_query(query, tuple(data.values()))

    def update(self, data: dict, condition: str, params: tuple):
        """
        Updates a record in the table.

        :param data: Dictionary of fields to update.
        :param condition: SQL condition for updating (e.g., "id = ?").
        :param params: Values for condition placeholders.
        """
        set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {self.table_name()} SET {set_clause} WHERE {condition}"
        self.db_manager.execute_query(query, tuple(data.values()) + params)

    def fetch_one(self, condition: str, params: tuple):
        """
        Fetches a single record based on a condition.
        """
        query = f"SELECT * FROM {self.table_name()} WHERE {condition} LIMIT 1"
        return self.db_manager.execute_query(query, params, fetchone=True)

    def fetch_all(self, condition: str = None, params: tuple = ()):
        """
        Fetches all records, optionally filtered by a condition.
        """
        query = f"SELECT * FROM {self.table_name()}"
        if condition:
            query += f" WHERE {condition}"
        return self.db_manager.execute_query(query, params, fetchall=True)

    def delete(self, condition: str, params: tuple):
        """
        Deletes records based on a condition.
        """
        query = f"DELETE FROM {self.table_name()} WHERE {condition}"
        self.db_manager.execute_query(query, params)
