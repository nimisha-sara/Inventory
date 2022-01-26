from fileinput import filename
import sqlite3

import os
import shutil

from docxtpl import DocxTemplate
import docx 
from docxcompose.composer import Composer

import win32api


def createTable():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS OLIVES
                        (ID             INTEGER   PRIMARY KEY   AUTOINCREMENT,
                        TRACK_NO         TEXT,
                        FROM_NAME        TEXT,
                        FROM_CONTACT       TEXT,
                        FROM_ADDRESS     TEXT,
                        DATE             TEXT,
                        SHIP_CITY      TEXT,
                        RECIEVER_NAME        TEXT,
                        RECIEVER_ADDRESS        TEXT,
                        RECIEVER_CONTACT        TEXT,
                        PRODUCTS_SELLING_PRICE     TEXT,
                        PRODUCTS_COST_PRICE    TEXT);''')
    connection.close()

    
def insert(track_no, from_name, from_contact, from_address, date, ship_city, reciever_name,
            reciever_address, reciever_contact, products_selling_price, products_cost_price):    
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO OLIVES
                        (track_no, from_name, from_contact, from_address, date, ship_city, reciever_name,
                            reciever_address, reciever_contact, products_selling_price, products_cost_price) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (track_no, from_name, from_contact, from_address, date, ship_city, reciever_name, reciever_address, reciever_contact, products_selling_price, products_cost_price))
    connection.commit()
    connection.close()


def delete(id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM OLIVES WHERE id = ?", (id,))
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
    return rows


def get(id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM  OLIVES WHERE id = ?", (id, ))
    rows = cursor.fetchall()
    return list(rows[0])


def bill_generate(selected_id):
    if os.path.exists('word_docs'):
        shutil.rmtree('word_docs')
    os.mkdir('word_docs')
    files = []
    for id in selected_id:
        text = get(id)
        doc = DocxTemplate("address_template.docx")
        context = { 
                    'from_name': text[2],  'reciever_name': text[7], 
                    'from_address': text[4], 'reciever_address': text[8],
                    'from_contact': text[3], 'reciever_contact': text[9]
                }
        doc.render(context)
        save_name = f"word_docs/{id}_word.docx"
        files.append(save_name)
        doc.save(save_name)
    
    result = docx.Document(files[0])
    composer = Composer(result)

    for i in range(1, len(files)):
        doc = docx.Document(files[i])

        if i != len(files) - 1:
            doc.add_page_break()

        composer.append(doc)

    composer.save("final_word.docx")


def printing_file(selected_items):
    bill_generate(selected_items)
    filename = "final_word.docx"
    win32api.ShellExecute(0, "print", filename, None, ".", 0)


def profits():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT PRODUCTS_SELLING_PRICE, PRODUCTS_COST_PRICE, DATE FROM  OLIVES")
    rows = cursor.fetchall()
    total_profits = 0
    selling_price = 0
    cost_price = 0
    for row in rows:
        print(row[2])
        total_profits += int(row[0]) - int(row[1])
        selling_price += int(row[0])
        cost_price += int(row[1])
    return {'no_of_sales': len(rows),'total_profits': total_profits, 'selling_price': selling_price, 'cost_price': cost_price}

print(profits())

