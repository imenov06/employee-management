import datetime
import random
import string
import sqlite3
from typing import List


class Employee:
    """Класс сотрудника с методами для работы с БД и расчета возраста"""

    def __init__(self, full_name: str, birth_date: str, gender: str):
        self.full_name = full_name
        self.birth_date = birth_date
        self.gender = gender

    def get_age(self) -> int:
        """Расчет полного возраста в годах"""
        birth_date = datetime.datetime.strptime(self.birth_date, '%Y-%m-%d').date()
        today = datetime.date.today()

        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age

    def save_to_db(self, conn: sqlite3.Connection) -> None:
        """Сохранение сотрудника в базу данных"""
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (full_name, birth_date, gender) VALUES (?, ?, ?)",
            (self.full_name, self.birth_date, self.gender)
        )
        conn.commit()

    @staticmethod
    def save_many_to_db(conn: sqlite3.Connection, employees: List['Employee']) -> None:
        """Пакетное сохранение сотрудников в базу данных"""
        cursor = conn.cursor()
        data = [(emp.full_name, emp.birth_date, emp.gender) for emp in employees]
        cursor.executemany(
            "INSERT INTO employees (full_name, birth_date, gender) VALUES (?, ?, ?)",
            data
        )
        conn.commit()

    @staticmethod
    def generate_random_employee() -> 'Employee':
        """Генерация случайного сотрудника"""
        # Генерация случайного ФИО (с равномерным распределением первых букв)
        first_letter = random.choice(string.ascii_uppercase)
        last_name = first_letter + ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 10)))

        first_name = random.choice(string.ascii_uppercase) + ''.join(
            random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
        middle_name = random.choice(string.ascii_uppercase) + ''.join(
            random.choices(string.ascii_lowercase, k=random.randint(5, 12)))

        full_name = f"{last_name} {first_name} {middle_name}"

        # Генерация случайной даты рождения (от 18 до 70 лет)
        today = datetime.date.today()
        days_in_year = 365.25
        max_age_days = int(70 * days_in_year)
        min_age_days = int(18 * days_in_year)
        random_days = random.randint(min_age_days, max_age_days)
        birth_date = today - datetime.timedelta(days=random_days)

        # Генерация пола (с равномерным распределением)
        gender = random.choice(["Male", "Female"])

        return Employee(full_name, birth_date.strftime('%Y-%m-%d'), gender)

    @staticmethod
    def generate_male_f_employee() -> 'Employee':
        """Генерация сотрудника-мужчины с фамилией на F"""
        last_name = "F" + ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 10)))

        first_name = random.choice(string.ascii_uppercase) + ''.join(
            random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
        middle_name = random.choice(string.ascii_uppercase) + ''.join(
            random.choices(string.ascii_lowercase, k=random.randint(5, 12)))

        full_name = f"{last_name} {first_name} {middle_name}"

        # Генерация случайной даты рождения (от 18 до 70 лет)
        today = datetime.date.today()
        days_in_year = 365.25
        max_age_days = int(70 * days_in_year)
        min_age_days = int(18 * days_in_year)
        random_days = random.randint(min_age_days, max_age_days)
        birth_date = today - datetime.timedelta(days=random_days)

        return Employee(full_name, birth_date.strftime('%Y-%m-%d'), "Male")