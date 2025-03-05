"""Module providing task_1 functions"""

from database import DatabaseManager
from database.test_data import employees_data


def main():
    """Main function to run the task_1."""
    conn_params = {
        'host': '0.0.0.0',
        'port': '5432',
        'database': 'task_1',
        'user': 'postgres',
        'password': 'pass'
    }
    table_columns = {
        'id': 'SERIAL PRIMARY KEY',
        'name': 'VARCHAR(255) NOT NULL',
        'position': 'VARCHAR(255) NOT NULL',
        'salary': 'DECIMAL(10, 2) NOT NULL'
    }
    with DatabaseManager(conn_params=conn_params) as db_manager:
        db_manager.create_table('employees', table_columns)
        for data in employees_data:
            db_manager.insert_data('employees', data)


if __name__ == "__main__":
    main()
