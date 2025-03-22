import sqlite3
import datetime
import time
from typing import List, Tuple


class Database:
    """Класс для работы с базой данных SQLite"""

    def __init__(self, db_name: str = "employees.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)

    def close(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        """Создание таблицы сотрудников"""
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            gender TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def get_all_employees(self) -> List[Tuple[str, str, str, int]]:
        """Получение всех сотрудников, отсортированных по ФИО, с уникальными ФИО+дата"""
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT DISTINCT full_name, birth_date, gender
        FROM employees
        ORDER BY full_name
        ''')

        employees_data = []
        for row in cursor.fetchall():
            full_name, birth_date, gender = row
            # Расчет возраста
            birth_date_obj = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
            today = datetime.date.today()
            age = today.year - birth_date_obj.year
            if (today.month, today.day) < (birth_date_obj.month, birth_date_obj.day):
                age -= 1

            employees_data.append((full_name, birth_date, gender, age))

        return employees_data

    def select_male_f_employees(self) -> List[Tuple[str, str, str, int]]:
        """Выборка сотрудников-мужчин с фамилией на F и замер времени выполнения"""
        start_time = time.time()

        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT full_name, birth_date, gender
        FROM employees
        WHERE gender = 'Male' AND full_name LIKE 'F%'
        ''')

        employees_data = []
        for row in cursor.fetchall():
            full_name, birth_date, gender = row
            # Расчет возраста
            birth_date_obj = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
            today = datetime.date.today()
            age = today.year - birth_date_obj.year
            if (today.month, today.day) < (birth_date_obj.month, birth_date_obj.day):
                age -= 1

            employees_data.append((full_name, birth_date, gender, age))

        end_time = time.time()
        execution_time = end_time - start_time

        return employees_data, execution_time

    def select_male_f_employees_optimized(self) -> List[Tuple[str, str, str, int]]:
        """Оптимизированная выборка сотрудников-мужчин с фамилией на F"""
        start_time = time.time()

        cursor = self.conn.cursor()

        # Используем более эффективный запрос с GLOB вместо LIKE
        cursor.execute('''
        SELECT full_name, birth_date, gender
        FROM employees
        WHERE gender = 'Male' AND full_name GLOB 'F*'
        ''')

        employees_data = []
        today = datetime.date.today()

        # Оптимизируем обработку результатов
        for row in cursor.fetchall():
            full_name, birth_date, gender = row
            # Более эффективный расчет возраста
            year, month, day = map(int, birth_date.split('-'))
            birth_date_obj = datetime.date(year, month, day)

            age = today.year - birth_date_obj.year
            if (today.month, today.day) < (birth_date_obj.month, birth_date_obj.day):
                age -= 1

            employees_data.append((full_name, birth_date, gender, age))

        end_time = time.time()
        execution_time = end_time - start_time

        return employees_data, execution_time

    def optimize_database(self):
        """Оптимизация базы данных для ускорения запросов"""
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA cache_size = 20000;")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_employees_gender_full_name ON employees(gender, full_name);')
        self.conn.commit()
        print("Оптимизация базы данных завершена")
