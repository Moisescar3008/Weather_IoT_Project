import sqlite3
import os
from typing import List, Tuple, Any

class DatabaseManager:
    def __init__(self) -> None:
        """
        Inicializa la conexión con la base de datos y verifica la existencia de las tablas.
        """
        # Asegura que la base de datos se ubique correctamente dentro del contenedor Docker
        self.location_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.db_path       = os.path.join(self.location_path, "static", "data", "database.db")

        # Crear tablas si no existen
        self.__create_tables()

    # =============== MÉTODOS PRIVADOS ===============
    def __connect(self) -> sqlite3.Connection:
        """
        Crea y devuelve una conexión a la base de datos.

        ### RETURNS:
        sqlite3.Connection: Objeto de conexión a la base de datos.
        """
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def __create_tables(self) -> None:
        """
        Crea las tablas necesarias si no existen en la base de datos.
        """
        queries= [
            """CREATE TABLE IF NOT EXISTS rain (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rain_detected BOOLEAN NOT NULL,
                intensity REAL NOT NULL,
                timestamp TEXT NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS temperature (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                timestamp TEXT NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS motion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                motion_detected BOOLEAN NOT NULL,
                timestamp TEXT NOT NULL
            )""",
            """CREATE TABLE IF NOT EXISTS pressure (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pressure REAL NOT NULL,
                altitude REAL NOT NULL,
                timestamp TEXT NOT NULL
            )"""
        ]

        conn = self.__connect()
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
        conn.commit()
        conn.close()

    # =============== MÉTODOS PÚBLICOS ===============
    def execute_query(self, query: str, params: Tuple[Any, ...] = ()) -> None:
        """
        Ejecuta una consulta SQL (INSERT, UPDATE, DELETE).

        ### ARGS:
        query (str): Consulta SQL a ejecutar.
        params (Tuple[Any, ...]): Parámetros opcionales para la consulta.

        ### RETURNS:
        None
        """
        conn = self.__connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_all(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
        """
        Ejecuta una consulta SELECT y devuelve todos los resultados.

        ### ARGS:
        query (str): Consulta SQL a ejecutar.
        params (Tuple[Any, ...]): Parámetros opcionales para la consulta.

        ### RETURNS:
        List[Tuple[Any, ...]]: Lista de tuplas con los resultados obtenidos.
        """
        conn = self.__connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    def insert_data(self, table: str, data: List[dict]) -> None:
        """
        Inserta un conjunto de datos en la tabla correspondiente.

        ### ARGS:
        table (str): Nombre de la tabla donde se insertarán los datos.
        data (List[dict]): Lista de diccionarios con los datos a insertar.

        ### RETURNS:
        None
        """
        conn = self.__connect()
        cursor = conn.cursor()

        queries = {
            "rain": "INSERT INTO rain (rain_detected, intensity, timestamp) VALUES (?, ?, ?)",
            "temperature": "INSERT INTO temperature (temperature, humidity, timestamp) VALUES (?, ?, ?)",
            "motion": "INSERT INTO motion (motion_detected, timestamp) VALUES (?, ?)",
            "pressure": "INSERT INTO pressure (pressure, altitude, timestamp) VALUES (?, ?, ?)"
        }

        if table not in queries:
            conn.close()
            raise ValueError(f"Tabla '{table}' no válida")

        values = [tuple(entry.values()) for entry in data]

        cursor.executemany(queries[table], values)
        conn.commit()
        conn.close()

    def delete_records(self, table: str, start_date: str = None, end_date: str = None) -> None:
        """
        Elimina registros de la tabla especificada. Puede eliminar todos los registros o solo los
        que estén dentro de un rango de fechas específico.

        ### ARGS:
        table (str): Nombre de la tabla de la cual se eliminarán los registros.
        start_date (str, opcional): Fecha de inicio en formato "yyyy-mm-dd". Solo se eliminarán registros desde esta fecha en adelante.
        end_date (str, opcional): Fecha de fin en formato "yyyy-mm-dd". Solo se eliminarán registros hasta esta fecha.

        ### RETURNS:
        None
        """
        valid_tables = {"rain", "temperature", "motion", "pressure"}
        
        if table not in valid_tables:
            raise ValueError(f"Tabla '{table}' no válida. Debe ser una de {valid_tables}")

        query = f"DELETE FROM {table}"
        params = []

        if start_date and end_date:
            query += " WHERE timestamp BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        elif start_date:
            query += " WHERE timestamp >= ?"
            params.append(start_date)
        elif end_date:
            query += " WHERE timestamp <= ?"
            params.append(end_date)

        conn = self.__connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

