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
        column_definitions = sql.SQL(', ').join(
            sql.SQL('{col_name} {data_type}').format(
                col_name=sql.Identifier(col_name),
                data_type=sql.SQL(data_type)
            ) for col_name, data_type in columns.items()
        )
        command = sql.SQL(
            'CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});'
        ).format(
            table_name=sql.Identifier(table_name),
            column_definitions=column_definitions
        )
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
        query = sql.SQL(
            'SELECT * FROM employees WHERE {condition};'
        ).format(
            condition=sql.SQL(condition)
        )
        return self.execute_query(query)

    def update(self, table_name, data, condition):
        """
        Update rows in the database that match a given condition.
        :param table_name: Name of the table to update.
        :param data: Dict with new values for the columns.
        :param condition: SQL condition (tuple: (sql_fragment, params)).
        """
        setter = sql.SQL(', ').join(
            sql.SQL('{col_name} = {col_data}').format(
                col_name=sql.Identifier(col_name),
                col_data=sql.Placeholder()
            ) for col_name in data.keys()
        )
        where = sql.SQL(condition[0]).format(
            *[sql.Placeholder()] * len(condition[1])
        )

        command = sql.SQL(
            'UPDATE {table} SET {setter} WHERE {where};'
        ).format(
            table=sql.Identifier(table_name),
            setter=setter,
            where=where
        )

        params = list(data.values()) + list(condition[1])

        self.execute_command(command, params)

    def delete(self, table_name, condition):
        """
        Delete rows in the database that match a given condition.
        :param table_name: Name of the table to delete from.
        :param condition: SQL condition (tuple: (sql_fragment, params)).
        """
        where = sql.SQL(condition[0]).format(
            *[sql.Placeholder()] * len(condition[1])
        )

        command = sql.SQL(
            'DELETE FROM {table} WHERE {where};'
        ).format(
            table=sql.Identifier(table_name),
            where=where
        )

        params = list(condition[1])

        self.execute_command(command, params)
