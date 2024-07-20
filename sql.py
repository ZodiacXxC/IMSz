import sqlite3

def insert_data(name, price, entry_date, category, barcode, total=1):
    with sqlite3.connect("main.db") as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute('''
            INSERT INTO products (Name, Price, Entry_Date, Category, Barcode, Total)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, price, entry_date, category, barcode, total))
        sql_connect.commit()

def get_all_data():
    with sqlite3.connect("main.db") as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute('''SELECT * FROM products''')
        return cursor.fetchall()

def get_all_bar():
    with sqlite3.connect("main.db") as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute('''SELECT Barcode FROM products''')
        return cursor.fetchall()

def delete_data(id_p):
    with sqlite3.connect("main.db") as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute('''DELETE FROM products WHERE ID = ?''', (id_p,))
        sql_connect.commit()

def update_data(id_,name, price, entry_date, category, barcode):
    with sqlite3.connect("main.db") as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute('''UPDATE products set Name = ? , Price = ? , Entry_Date = ? , Category = ? , Barcode = ?  WHERE ID = ?''', (name,price,entry_date,category,barcode,id_))
        sql_connect.commit()

def insert_into_cat(id_p):
    with sqlite3.connect("main.db") as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute('''UPDATE products SET Total = Total + 1 WHERE Barcode = ?''', (id_p,))
        sql_connect.commit()

def sell_product(id_p):
    with sqlite3.connect("main.db") as sql_connect:
        cursor = sql_connect.cursor()
        cursor.execute('''UPDATE products SET Total = Total - 1 WHERE ID = ?''', (id_p,))
        sql_connect.commit()


def get_cat(cat):
    with sqlite3.connect("main.db") as sql_connect:
        cursor = sql_connect.cursor()
        data = cursor.execute(f'''SELECT * FROM products WHERE Category ="{cat}"''')
        return data

# Create the products table
with sqlite3.connect("main.db") as sql_connect:
    cursor = sql_connect.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Price REAL NOT NULL,
            Entry_Date TEXT NOT NULL,
            Category TEXT NOT NULL,
            Total INTEGER NOT NULL,       
            Barcode TEXT NOT NULL
        )
    ''')
    sql_connect.commit()
