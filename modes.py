from employee import Employee
from database import Database


class ApplicationModes:
    """Класс, реализующий все режимы работы приложения"""

    def __init__(self, db_name: str = "employees.db"):
        """Инициализация с возможностью указать имя БД"""
        self.db_name = db_name

    def create_table(self):
        """Режим 1: Создание таблицы"""
        db = Database(self.db_name)
        db.create_table()
        print("Таблица успешно создана")
        db.close()

    def add_employee(self, full_name: str, birth_date: str, gender: str):
        """Режим 2: Добавление сотрудника"""
        try:
            employee = Employee(full_name, birth_date, gender)
            db = Database(self.db_name)
            employee.save_to_db(db.conn)
            print(f"Сотрудник добавлен: {full_name}, Возраст: {employee.get_age()}")
            db.close()
        except Exception as e:
            print(f"Ошибка при добавлении сотрудника: {e}")

    def list_employees(self):
        """Режим 3: Вывод всех сотрудников, отсортированных по ФИО"""
        try:
            db = Database(self.db_name)
            employees = db.get_all_employees()

            print(f"{'ФИО':<30} {'Дата рождения':<12} {'Пол':<8} {'Возраст':<5}")
            print("-" * 60)

            for full_name, birth_date, gender, age in employees:
                print(f"{full_name:<30} {birth_date:<12} {gender:<8} {age:<5}")

            print(f"\nВсего сотрудников: {len(employees)}")
            db.close()
        except Exception as e:
            print(f"Ошибка при выводе списка сотрудников: {e}")

    def generate_data(self):
        """Режим 4: Генерация 1,000,000 случайных сотрудников + 100 спец. сотрудников"""
        try:
            db = Database(self.db_name)
            batch_size = 10000

            print("Генерация 1,000,000 случайных сотрудников...")

            for i in range(0, 1000000, batch_size):
                employees_batch = [Employee.generate_random_employee() for _ in range(batch_size)]
                Employee.save_many_to_db(db.conn, employees_batch)
                print(f"Сгенерировано и сохранено {i + batch_size} сотрудников")

            print("Генерация 100 сотрудников-мужчин с фамилией на 'F'...")
            f_male_employees = [Employee.generate_male_f_employee() for _ in range(100)]
            Employee.save_many_to_db(db.conn, f_male_employees)

            print("Генерация данных завершена")
            db.close()
        except Exception as e:
            print(f"Ошибка при генерации данных: {e}")

    def query_performance(self):
        """Режим 5: Тест производительности запроса для сотрудников-мужчин с фамилией на F"""
        try:
            db = Database(self.db_name)
            employees, execution_time = db.select_male_f_employees()

            print(f"Запрос выполнен за {execution_time:.6f} секунд")
            print(f"Найдено {len(employees)} сотрудников-мужчин с фамилией на 'F'")

            print(f"\n{'ФИО':<30} {'Дата рождения':<12} {'Пол':<8} {'Возраст':<5}")
            print("-" * 60)

            for full_name, birth_date, gender, age in employees[:10]:  # Показываем только первые 10 результатов
                print(f"{full_name:<30} {birth_date:<12} {gender:<8} {age:<5}")

            if len(employees) > 10:
                print("... (показаны только первые 10 результатов)")

            db.close()
        except Exception as e:
            print(f"Ошибка в тесте производительности: {e}")

    def optimize(self):
        """Режим 6: Оптимизация базы данных и тест производительности"""
        try:
            db = Database(self.db_name)

            # Тест производительности до оптимизации
            print("Производительность до оптимизации:")
            employees_before, time_before = db.select_male_f_employees()
            print(f"Запрос выполнен за {time_before:.6f} секунд")
            print(f"Найдено {len(employees_before)} сотрудников-мужчин с фамилией на 'F'")

            # Оптимизация базы данных
            print("\nОптимизация базы данных...")
            db.optimize_database()

            # Тест производительности после оптимизации с улучшенным запросом
            print("\nПроизводительность после оптимизации:")
            employees_after, time_after = db.select_male_f_employees_optimized()
            print(f"Запрос выполнен за {time_after:.6f} секунд")
            print(f"Найдено {len(employees_after)} сотрудников-мужчин с фамилией на 'F'")

            # Расчет улучшения
            improvement = (time_before - time_after) / time_before * 100
            print(f"\nУлучшение производительности: {improvement:.2f}%")
            print(f"Время до оптимизации: {time_before:.6f} секунд")
            print(f"Время после оптимизации: {time_after:.6f} секунд")

            print("\nОбъяснение оптимизации:")
            print("1. Создан индекс по полям gender и full_name для быстрого поиска")
            print("2. Увеличен размер кэша SQLite с стандартного до 20000 страниц")
            print("3. Использован оператор GLOB вместо LIKE для более эффективного сравнения")
            print("4. Оптимизирована обработка дат в результатах запроса")

            db.close()
        except Exception as e:
            print(f"Ошибка при оптимизации: {e}")
