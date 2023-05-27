import sqlite3


def createTable():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS OLIVES
                        (ID             INTEGER   PRIMARY KEY ,
                        CUSTOMER         TEXT,
                        ADDRESS        TEXT,
                        CONTACT       TEXT,
                        PRODUCTS     TEXT,
                        QUANTITY             TEXT,
                        RATES      TEXT,
                        TOTAL        NUMBER,
                        PRODUCT_COUNT        NUMBER,
                        DATE        TEXT,
                        CITY_STATE     TEXT);''')
    connection.close()


def insert(customer, address, contact, products, quantity, rates, total, product_count, date, city_state):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO OLIVES
                        (customer, address, contact, products, quantity, rates, total, product_count, date, city_state) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (customer, address, contact, products, quantity, rates, total, product_count, date, city_state))
    connection.commit()
    connection.close()


def view():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM OLIVES")
    rows = cursor.fetchall()
    connection.close()
    return list(rows)


def get(id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM  OLIVES WHERE id = ?", (id, ))
    rows = cursor.fetchall()
    return list(rows[0])


def get_customers():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT customer FROM OLIVES")
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_address():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT address FROM OLIVES")
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_contact():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT contact FROM OLIVES")
    rows = cursor.fetchall()
    connection.close()
    return rows
