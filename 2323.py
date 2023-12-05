import sqlite3


class User:
    def __init__(self,user_id,name1,surname1,login,password):
        self.user_id = user_id
        self.name1 = name
        self.surname1 = surname
        self.login = login
        self.password = password

class Tovar:
    def __init__(self, tovar_id,brand,model,year ):
        self.tovar_id = tovar_id
        self.brand = brand
        self.model = model
        self.year = year




class Administrator:
    def __init__(self,Administrator_id,surname,name):
        self.administrator_id = administrator_id
        self.surname = surname
        self.name = name


class Order:
    def __init__(self, order_id, user, product):
        self.id = order_id
        self.user = user
        self.product = product



class DataBase:
    conn = sqlite3.connect('sale_car.db')
    cursor = conn.cursor()


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        surname1 TEXT NOT NULL,
        name1 TEXT NOT NUILL,
        login TEXT NOT NULL,
        passsword TEXT NOT NULL
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISITS tovars(
        id INTERGER PRIMARY KEY,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        year TEXT NOT NULL
          
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXESITS administrator(
        id INTERGER PRIMARY KEY,
        surname TEXT NOT NULL,
        name TEXT NOT NULL
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXEITS order(
        id INTERGER PRIMARY KEY,
        user TEXT NOT NULL,
        pdroduct TEXT NOT NULL
    
    ''')

    conn.commit()

class Add:
    @classmethod
    def add_user(cls,user):
         cls.cursor.execute('''
             INSERT INTO users (name1,surname1,login, password)
             VALUES (?, ?, ?, ?)
         ''', (user.name, user.surname, user.login, user.password))
         cls.conn.commit()

    @classmethod
    def add_tovar(cls):
        cls.cursor.execute('''
            INSERT INTO tovars (brand,model,year)
            VALUES(?,?,?)
        ''',(tovar.brand, tovar.model,tovar.year))
        cls.conn.commit()


    @classmethod
    def add_administrator(cls):
        cls.cursor.execute('''
            INSERT INTO administrators(surname,name)
            VALUES(?,?)
        ''',(administrator.surname,administrator.name))


    @classmethod
    def add_order(cls):
        cls.cursor.execute('''
            INSERT INTO orders(user,product)
            VALUES(?,?)
        ''', (orders.user, orders.product))


