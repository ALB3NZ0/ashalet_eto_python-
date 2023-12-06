import sqlite3
class User:
    def __init__(self, user_id, name, surname, login, password, role):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.login = login
        self.password = password
        self.role = role

class Tovar:
    def __init__(self, tovar_id, brand, model, year, product_count, price):
        self.tovar_id = tovar_id
        self.brand = brand
        self.model = model
        self.year = year
        self.product_count = product_count
        self.price = price

class Administrator:
    def __init__(self, administrator_id, surname, name):
        self.administrator_id = administrator_id
        self.surname = surname
        self.name = name

class Order:
    def __init__(self, order_id, user_id, product_id):
        self.order_id = order_id
        self.user_id = user_id
        self.product_id = product_id

class DataBase:
    conn = sqlite3.connect('sale_car.db')
    cursor = conn.cursor()
    @classmethod
    def create_tables(cls):
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            surname TEXT NOT NULL,
            name TEXT NOT NULL,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )''')
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS tovars (
            id INTEGER PRIMARY KEY,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            product_count INTEGER NOT NULL,
            price REAL NOT NULL
        )''')
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS administrators (
            id INTEGER PRIMARY KEY,
            surname TEXT NOT NULL,
            name TEXT NOT NULL
        )''')
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES tovars (id)
        )''')
        cls.conn.commit()

    @classmethod
    def fetch_user(cls, surname, password):
        cls.cursor.execute('''SELECT * FROM users WHERE surname = ? AND password = ?''', (surname, password))
        user_data = cls.cursor.fetchone()
        if user_data:
            user_id, name, surname, login, password, role = user_data
            return User(user_id, name, surname, login, password, role)
        else:
            return None

    @classmethod
    def add_user(cls, user):
        cls.cursor.execute('''INSERT INTO users (name, surname, login, password, role) VALUES (?, ?, ?, ?, ?)''', (user.name, user.surname, user.login, user.password, user.role))
        cls.conn.commit()

    @classmethod
    def add_tovar(cls, tovar):
        cls.cursor.execute('''INSERT INTO tovars (brand, model, year, product_count, price) VALUES (?, ?, ?, ?, ?)''', (tovar.brand, tovar.model, tovar.year, tovar.product_count, tovar.price))
        cls.conn.commit()

    @classmethod
    def add_administrator(cls, administrator):
        cls.cursor.execute('''INSERT INTO administrators (surname, name) VALUES (?, ?)''', (administrator.surname, administrator.name))
        cls.conn.commit()

    @classmethod
    def add_order(cls, order):
        cls.cursor.execute('''INSERT INTO orders (user_id, product_id) VALUES (?, ?)''', (order.user_id, order.product_id))
        cls.conn.commit()

    @classmethod
    def change_order(cls, order_id, new_products):
        cls.cursor.execute('''UPDATE orders SET product_id = ? WHERE id = ?''', (new_products, order_id))
        cls.conn.commit()

    @classmethod
    def delete_order(cls, order_id):
        cls.cursor.execute('''DELETE FROM orders WHERE id = ?''', (order_id,))
        cls.conn.commit()

class Menu:
    @staticmethod
    def register():
        surname = input("Введите фамилию пользователя: ")
        password = input("Введите пароль: ")
        role = input("Выберите роль (Клиент/Администратор): ")
        name = input("Введите ваше полное имя: ")
        user = User(None, name, surname, None, password, role)
        DataBase.add_user(user)
        print("Регистрация прошла успешно!")

    @staticmethod
    def login():
        surname = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        user = DataBase.fetch_user(surname, password)
        if user:
            return user
        else:
            print("Неверное имя пользователя или пароль.")
            return None

    @staticmethod
    def view_products():
        # Извлекаем товары из базы данных
        DataBase.cursor.execute("SELECT * FROM tovars")
        products = DataBase.cursor.fetchall()

        # Выводим информацию о товарах
        if products:
            print("Список товаров:")
            for product in products:
                tovar_id, brand, model, year, product_count, price = product
                print(f"ID: {tovar_id}, Бренд: {brand}, Модель: {model}, Год выпуска:{year}, Количество: {product_count}, Цена: {price}")
        else:
            print("В базе данных нет товаров.")

    @staticmethod
    def add_to_product_count():
        tovar_id = input("Введите ID товара, который хотите добавить в корзину: ")
        quantity = int(input("Введите количество товара: "))

        # Проверка наличия товара по ID
        DataBase.cursor.execute("SELECT * FROM tovars WHERE id = ?", (tovar_id,))
        product = DataBase.cursor.fetchone()

        if product:
            user_id = 1
            order = Order(None, user_id, tovar_id)

            # Добавляем заказ в базу данных
            DataBase.add_order(order)
            print("Товар успешно добавлен в корзину!")
        else:
            print("Товар с указанным ID не найден.")

    @staticmethod
    def change_order():
        order_id = input("Введите ID заказа, который хотите изменить: ")
        new_products = input("Введите новый список товаров: ")

        # Проверка наличия заказа по ID
        DataBase.cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = DataBase.cursor.fetchone()

        if order:
            # Если заказ найден, изменяем его
            DataBase.change_order(order_id, new_products)
            print("Заказ успешно изменен!")
        else:
            print("Заказ с указанным ID не найден.")

    @staticmethod
    def delete_order():
        order_id = input("Введите ID заказа, который хотите удалить: ")

        # Проверка наличия заказа по ID
        DataBase.cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = DataBase.cursor.fetchone()

        if order:
            # Если заказ найден, удаляем его
            DataBase.delete_order(order_id)
            print("Заказ успешно удален!")
        else:
            print("Заказ с указанным ID не найден.")

    @staticmethod
    def client_interface():
        print("Добро пожаловать в интерфейс клиента!")
        while True:
            choice = input(
                "1. Просмотр товаров\n2. Добавить товар в корзину\n3. Изменить заказ\n4. Удалить заказ\n5. Изменить данные\n6. Выйти\nВыберите действие: ")
            if choice == "1":
                Menu.view_products()
            elif choice == "2":
                Menu.add_to_product_count()
            elif choice == "3":
                Menu.change_order()
            elif choice == "4":
                Menu.delete_order()
                pass
            elif choice == "6":
                return  # Возвращаемся в главное меню
            else:
                print("Неверный ввод. Пожалуйста, выберите корректное действие.")

    @staticmethod
    def main():
        while True:
            # Main menu
            choice = input("1. Регистрация\n2. Авторизация\n3. Выход\nВыберите действие: ")

            if choice == "1":
                Menu.register()
            elif choice == "2":
                user = Menu.login()
                if user and user.role == "Клиент":
                    Menu.client_interface()
                elif user and user.role == "Сотрудник":
                    Menu.employee_interface()
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите корректное действие.")

if __name__ == "__main__":
    DataBase.create_tables()

    BMW_E34 = Tovar(None, "BMW", "E34", 1989, 10, 3000000)
    BMW_X6 = Tovar(None, "BMW", "X6", 2023, 5, 23000000)
    BMW_M5_F90 = Tovar(None, "BMW", "M5_F90", 2020, 3, 1500000)
    Mercedes_Benz_Cls = Tovar(None, "Mercedes Benz", "Cls", 2017, 8, 10000000)
    Toyota_Mark2 = Tovar(None, "Toyota", "Mark2", 1994, 15, 30000000)

    # Добавление в базу данных
    DataBase.add_tovar(BMW_E34)
    DataBase.add_tovar(BMW_X6)
    DataBase.add_tovar(BMW_M5_F90)
    DataBase.add_tovar(Mercedes_Benz_Cls)
    DataBase.add_tovar(Toyota_Mark2)


    Menu.main()
