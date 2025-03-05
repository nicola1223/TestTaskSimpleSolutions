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
        # Создает таблицу `employees` с полями:
        # `id`, `name`, `position`, `salary`.
        db_manager.create_table('employees', table_columns)
        # Добавляет в таблицу 5 тестовых записей.
        for data in employees_data:
            db_manager.insert_data('employees', data)
        # Выполняет запрос, который выводит всех сотрудников,
        # у которых зарплата больше 50 000.
        print(db_manager.search('salary > 50000'))
        # Обновляет зарплату сотрудника с именем "Иван" до 60 000.
        db_manager.update(
            'employees',
            {'salary': 60000.00},
            ('name = %s', ('Иван',))
        )
        # Удаляет сотрудника с именем "Анна".
        db_manager.delete(
            'employees',
            ('name = %s', ('Анна',))
        )


if __name__ == "__main__":
    main()
