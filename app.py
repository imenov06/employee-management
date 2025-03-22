import sys
from modes import ApplicationModes


class Application:

    def __init__(self, db_name: str = "employees.db"):
        self.modes = ApplicationModes(db_name)

    def print_usage(self):
        print("Использование: python app.py <режим> [аргументы]")
        print("Режимы:")
        print("  1: Создание таблицы")
        print("  2: Добавление сотрудника (требуются ФИО, дата рождения, пол)")
        print("  3: Вывод всех сотрудников")
        print("  4: Генерация случайных данных")
        print("  5: Тест производительности")
        print("  6: Оптимизация базы данных")

    def run(self, args):
        if len(args) < 2:
            self.print_usage()
            return

        mode = args[1]

        try:
            if mode == "1":
                self.modes.create_table()
            elif mode == "2":
                if len(args) < 5:
                    print("Использование: python app.py 2 \"<ФИО>\" <дата_рождения> <пол>")
                    return
                full_name = args[2]
                birth_date = args[3]
                gender = args[4]
                self.modes.add_employee(full_name, birth_date, gender)
            elif mode == "3":
                self.modes.list_employees()
            elif mode == "4":
                self.modes.generate_data()
            elif mode == "5":
                self.modes.query_performance()
            elif mode == "6":
                self.modes.optimize()
            else:
                print(f"Неизвестный режим: {mode}")
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)