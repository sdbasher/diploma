import datetime
import csv


class Person:
    def __init__(self, first_name, last_name='', middle_name='', birth_date='', death_date='', gender=''):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.birth_date = self.parse_date(birth_date)
        self.death_date = self.parse_date(death_date) if death_date else None
        self.gender = gender

    @staticmethod
    def parse_date(date_str):
        for fmt in ('%d.%m.%Y', '%d %m %Y', '%d/%m/%Y', '%d-%m-%Y'):
            try:
                return datetime.datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        raise ValueError('Invalid date format')

    def age(self):
        if self.death_date:
            end_date = self.death_date
        else:
            end_date = datetime.date.today()
        return (end_date - self.birth_date).days // 365

    def __str__(self):
        gender_str = 'чоловік' if self.gender == 'm' else 'жінка'
        death_info = f'Помер: {self.death_date.strftime("%d.%m.%Y")}' if self.death_date else ''
        return f'{self.first_name} {self.last_name} {self.middle_name} {self.age()} років, {gender_str}. Народився: {self.birth_date.strftime("%d.%m.%Y")}. {death_info}'


class Database:
    def __init__(self):
        self.records = []

    def add_person(self, first_name, last_name, middle_name, birth_date, death_date, gender):
        p = Person(first_name, last_name, middle_name, birth_date, death_date, gender)
        self.records.append(p)

    def search(self, query):
        results = []
        query = query.lower()
        for person in self.records:
            if (query in person.first_name.lower() or
                    query in person.last_name.lower() or
                    query in person.middle_name.lower()):
                results.append(person)
        return results

    def load_from_file(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            self.records = []
            for row in reader:
                self.add_person(*row)

    def save_to_file(self, filename):
        with open(filename, mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            for person in self.records:
                writer.writerow([person.first_name, person.last_name, person.middle_name,
                                 person.birth_date.strftime('%d.%m.%Y'),
                                 person.death_date.strftime('%d.%м.%Y') if person.death_date else '',
                                 person.gender])


def print_menu():
    print("\nМеню:")
    print("1. Додати нову людину")
    print("2. Пошук людини")
    print("3. Завантажити дані з файлу")
    print("4. Зберегти дані у файл")
    print("5. Вийти")


def main():
    db = Database()
    while True:
        print_menu()
        choice = input("Оберіть пункт меню: ")

        if choice == '1':
            first_name = input("Ім'я: ")
            last_name = input("Прізвище: ")
            middle_name = input("По-батькові: ")
            birth_date = input("Дата народження (дд.мм.рррр): ")
            death_date = input("Дата смерті (дд.мм.рррр, залиште порожнім, якщо жива): ")
            gender = input("Стать (m/f): ")
            db.add_person(first_name, last_name, middle_name, birth_date, death_date, gender)

        elif choice == '2':
            query = input("Введіть ім'я для пошуку: ")
            results = db.search(query)
            for person in results:
                print(person)

        elif choice == '3':
            filename = input("Введіть назву файлу для завантаження: ")
            db.load_from_file(filename)
            print("Дані завантажено.")

        elif choice == '4':
            filename = input("Введіть назву файлу для збереження: ")
            db.save_to_file(filename)
            print("Дані збережено.")

        elif choice == '5':
            break

        else:
            print("Неправильний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
