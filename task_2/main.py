"""Module providing task_2 functions"""


def data_manipulation(data: list):
    """Function to manipulate data according to the given requirements."""
    ans = {}
    ans['names_filter'] = list(filter(lambda x: x['salary'] > 50000, data))
    ans['average_salary'] = sum(map(lambda x: x['salary'], data)) / len(data)
    ans['sorted_employees'] = sorted(
        data, key=lambda x: x['salary'], reverse=True
    )
    return ans


def main():
    """Main function to run the task_2."""
    employees = [
        {"name": "Иван", "position": "разработчик", "salary": 55000},
        {"name": "Анна", "position": "аналитик", "salary": 48000},
        {"name": "Петр", "position": "тестировщик", "salary": 52000},
    ]
    print(data_manipulation(employees))


if __name__ == "__main__":
    main()
