import pyodbc
from typing import List, Tuple, Dict, Any

from DatabaseQueryError import DatabaseQueryError

DB_CONNECTION_CONFIG = {
    "DSN": "AppDB",
    "Uid": "su",
    "Pwd": "LUDRHQ2g4"
}

class DatabaseController:
    def __init__ (self, config: Dict[str, str]) -> None:
        self.config = config

    def get_connection_string(self) -> str:
        return ";".join([f"{key}={value}" for key, value in self.config.items()])

    def fetch_data (self, query : str, params: Tuple[Any, ...] = ()) -> Tuple[List[str], List[Tuple[Any, ...]]]:
        try:
            conn  = pyodbc.connect(self.get_connection_string())
            cursor  = conn.cursor()
            cursor.execute(query, params)
            headers  = [column[0] for column in cursor.description]
            rows : List[Tuple[Any, ...]] = cursor.fetchall()
            conn.close()
            return headers, rows
        except pyodbc.Error as e:
            raise DatabaseQueryError(f"Error during fetching data: {e}")

    def execute_query(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        try:
            conn = pyodbc.connect(self.get_connection_string())
            cursor  = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            conn.close()
        except pyodbc.Error as e:
            raise DatabaseQueryError(f"Error during executing query: {e}")



