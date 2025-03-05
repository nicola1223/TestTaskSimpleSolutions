"""Module provides a simple interface for interacting with a PostgreSQL db."""

import psycopg2
from psycopg2 import sql


class DatabaseManager:
    """Class for managing a PostgreSQL database."""
    def __init__(self, conn_params):
        self.con_params = conn_params
        self.conn = None
        self.cur = None

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        self.conn = psycopg2.connect(**self.con_params)
        self.cur = self.conn.cursor()

    def close(self):
        """Close the connection to the PostgreSQL database."""
        self.cur.close()
        self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def execute_query(self, query):
        """
        Execute a SQL query and return the result.
        :param query: SQL query to execute.
        :return: Result of the query.
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def execute_command(self, command, params=None):
        """
        Execute a SQL command (like CREATE TABLE, INSERT INTO, etc.).
        :param command: SQL command to execute.
        """
        self.cur.execute(command, params or ())
        self.conn.commit()

    def create_table(self, table_name, columns):
        """
        Create a new table in the database.
        :param table_name: Name of the table to create.
        :param columns: Dict with a column names and its types.
        """
        column_definitions = ', '.join(
            f'{col[0]} {col[1]}' for col in columns.items()
        )
        command = 'CREATE TABLE if NOT EXISTS ' \
            f'{table_name} ({column_definitions});'
        self.execute_command(command)

    def insert_data(self, table_name, data):
        """
        Insert data into a table.
        :param table_name: Name of the table to insert data into.
        :param data: Dict, where each tuple represents a row.
        """
        values = list(data.values())
        command = sql.SQL(
            "INSERT INTO {table} ({fields}) VALUES ({values})"
        ).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, data.keys())),
            values=sql.SQL(', ').join([sql.Placeholder()] * len(data))
        )
        self.execute_command(command, values)
        self.conn.commit()

    def search(self, condition):
        """
        Search for rows in the database that match a given condition.
        :param condition: SQL condition to search for.
        :return: Result of the search query.
        """
        query = f"SELECT * FROM employees WHERE {condition};"
        return self.execute_query(query)
