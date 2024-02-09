import sqlite3
import sys
import time
import os
import csv
import datetime

password_entered = 'false'
color = 'default'
currency = 'us'
exchange_rate = float(1.0)
sign = '$'

################## Text Based User Interface ####################


def currency_changer():
    global currency, exchange_rate, sign
    if currency == 'us':
        exchange_rate = float(1.0)
        sign = '$'
    elif currency == 'rupee':
        exchange_rate = float(76.38)
        sign = '₹'
    elif currency == 'yen':
        exchange_rate = float(116.00)
        sign = '¥'


def print_colored(text):
    global color
    if color == 'red':
        print("\u001b[31m%s\u001b[0m" % text)
    elif color == 'blue':
        print("\u001b[34m%s\u001b[0m" % text)
    elif color == 'pink':
        print("\u001b[35m%s\u001b[0m" % text)
    elif color == 'default':
        print("\u001b[37m%s\u001b[0m" % text)


def password():
    global password_entered
    print_colored("To access data base, a password will be required\n")
    print_colored('Please Enter Your Password')
    password = input("")
    if '2' == password:
        print_colored("The password was correct\n")
        password_entered = 'true'
        time.sleep(1.2)
        show_menu()
        handle_choice()
    else:
        print_colored('incorrect password, please try again\n')


def show_menu():
    print_colored("\nProduct Table Menu")
    print_colored("1. (Re)Create product table")
    print_colored("2. Add new product")
    print_colored("3. Update existing product")
    print_colored("4. Delete existing product")
    print_colored("5. Find products")
    print_colored("6. List products")
    print_colored("7. CSV file options")
    print_colored("8. Settings")
    print_colored("0. To exit")


def handle_choice():
    print_colored("Please select an option: ")
    choice = input("")
    if '0' == choice:
        print_colored("Bye!")
        sys.exit()
    elif "1" == choice:
        print_colored("\nRe)Create Product Table selected")
        create_product_table_UI()
    elif "2" == choice:
        print_colored("\nAdd product")
        insert_UI()
    elif "3" == choice:
        print_colored("\nUpdate product")
        update_UI()
    elif "4" == choice:
        print_colored("\nDelete product")
        delete_UI()
    elif "5" == choice:
        print_colored("\nFind products")
        select_products_UI()
    elif "6" == choice:
        print_colored("\nList products")
        list_products_UI()
    elif "7" == choice:
        print_colored("\nCSV file")
        db_csv_UI()
    elif "8" == choice:
        print_colored("\nSettings selected")
        settings_UI()
    else:
        print_colored("\nPlease select again.")

################## DB SQL Functionality ####################
# CREATE DB AND TABLE


def create_product_table_UI():
    create_table()


def create_table():
    db_name = "coffee_shop.db"
    sql = """create table Product
            (ProductID integer,
            Name text,
            Price real,
            primary key(ProductID))"""
    table_name = "Product"

    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master where name=?", (table_name,))
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1:
            print_colored("The table {0} already exists, do you wish to recreate it? (y/n): ".format(table_name))
            response = input("")
            if response == 'y':
                keep_table = False
                print_colored("The {0} table will be recreated - all existing data will be lost.".format(table_name))
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
                time.sleep(0.5)
            else:
                print_colored("The existing table was kept.\n")
                time.sleep(0.5)
        else:
            keep_table = False
            print_colored("A new table was created.\n")
            time.sleep(0.5)

        # create the table if required (not keeping old one)
        if not keep_table:
            cursor.execute(sql)
            db.commit()


# ADD #
def insert_data(values):
    global sign
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        sql = "insert into Product (Name, Price) values (?,?)"
        cursor.execute(sql, values)
        db.commit()
        print_colored("%s has been added at the price of %s%s\n" % (values[0], sign, values[1]))
        time.sleep(0.5)


def insert_UI():
    print_colored("Please enter name of new product.")
    product_name_l = input()
    while len(product_name_l) == 0:
        print_colored("Cannot leave product name blank, please try again")
        product_name_l = input()
    product_name = product_name_l.title()
    print_colored("Please enter price of %s: " % product_name)
    try:
        product_price = "{:.2f}".format(float(input()))
        product = (product_name, product_price)
        insert_data(product)
    except ValueError:
        print_colored("Please enter a valid price\n\n")
        while product_name == ValueError:
            product_price = "{:.2f}".format(float(input()))
            product = (product_name, product_price)
            insert_data(product)


# UPDATE #
def update_product(data):
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        sql = "update Product set Name=?, Price=? where ProductID=?"
        cursor.execute(sql, data)
        db.commit()
        print_colored("Product info has been updated.\n")
        time.sleep(0.5)


def update_UI():
    print_colored("Please enter product ID to edit.")
    product_ID = input()
    print_colored("Please enter the new name: ")
    product_name = input()
    product_n = product_name.title()
    while len(product_name) == 0:
        print_colored("Cannot leave product name blank, please try again")
        product_name = input()
        product_n = product_name.title()
    print_colored("Please enter price of %s: " % product_n)
    try:
        product_price = "{:.2f}".format(float(input()))
        data = (product_name, product_price, product_ID)
        update_product(data)
        while product_price == ValueError:
            product_price = "{:.2f}".format(float(input()))
            data = (product_name, product_price, product_ID)
            update_product(data)
    except Exception:
        print_colored("Please try again\n\n")


# SELECT #
def select_product_ID(id):
    global exchange_rate, sign
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select ProductID,Name,Price from Product where ProductID=?", (id,))
        product = cursor.fetchone()
        time.sleep(0.2)
        product_price = f'{product[2] * exchange_rate:.2f}'
        print_colored(f'ID: {product[0]}    Name: {product[1]}     Price: %s{product_price} ' % sign)


def select_product_name(name):
    global exchange_rate, sign
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select ProductID,Name,Price from Product where Name=?", (name,))
        product = cursor.fetchone()
        time.sleep(0.2)
        product_price = f'{product[2] * exchange_rate:.2f}'
        print_colored(f'ID: {product[0]}    Name: {product[1]}     Price: %s{product_price} ' % sign)


def select_price_range(price_range_x, price_range_y):
    global exchange_rate, sign
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select Price, Name from Product WHERE Price >= ? AND Price <= ? order by Price ASC", (price_range_x, price_range_y,))
        products = cursor.fetchall()
        time.sleep(0.2)
        for products in products:
            products_price = f'{products[0] * exchange_rate:.2f}'
            print_colored(f"Price: %s{products_price}     Name: {products[1]} " % sign)


def select_products_UI():
    print_colored("Enter \'id' to search list by the Product ID, \'name' search list by name or \'range' to search list by price range")
    choice = input()
    choice = choice.lower()
    choice = choice.strip()
    if choice == 'id':
        try:
            print_colored("Please enter product ID to find.")
            product_ID = int(input())
            select_product_ID(product_ID)
        except ValueError:
            print_colored("Not a valid ID. Please try again")

    elif choice == 'name':
        print_colored("Please enter product name to find.\n")
        product_name = str(input()).title()
        select_product_name(product_name)

    elif choice == 'range':
        print_colored('Please enter the lower number of the range of the price of products')
        price_range_x = "{:.2f}".format(float(input()))
        print_colored('Please enter the higher number of the range of the price of products')
        price_range_y = "{:.2f}".format(float(input()))
        if price_range_x > price_range_y:
            print_colored("First value in range is larger than the second value")
        else:
            select_price_range(price_range_x, price_range_y)
    else:
        print_colored("Please select again.\n")
    print_colored("\nPress enter to continue.\n")
    input()


# DELETE #
def delete_product_ID(data):
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        sql = "delete from Product where ProductID=?"
        cursor.execute(sql, data)
        print_colored("Product ID %s has been deleted" % data[0])
        db.commit()


def delete_product_name(name):
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        sql = "delete from Product where Name=?"
        cursor.execute(sql, name)
        print_colored("%s has been deleted" % name[0])
        db.commit()


def delete_UI():
    print_colored("Enter \'id' to delete product by Product ID, or \'name' delete product by name")
    choice = input()
    choice = choice.lower()
    choice = choice.strip()
    if choice == 'id':

        try:
            print_colored("Please enter product ID to delete.")
            product_ID = int(input())
            data = (product_ID,)
            delete_product_ID(data)

        except ValueError:
            print_colored("Not a valid ID. Please try again")

    elif choice == 'name':
        print_colored("Please enter product name to delete.")
        product_name = str(input()).title()
        data = (product_name,)
        delete_product_name(data)
    else:
        print_colored("Please select again.\n")
    print_colored("Press enter to continue.")
    input()


# LIST sort/order products
def list_products_UI():
    global exchange_rate, sign
    print_colored((
     "Enter \'alphasc' for an alphabetically ascending ordered list, \'alphadsc' for an "
     "alphabetically descending list,\n\'numasc' for numerically ascending list by price and \'numdsc'for "
     "a numerically descending list, \n\'idasc' for ascending ProductID and \'iddsc' for descending"
     " ProductID list"))
    choice = input()
    choice = choice.lower()
    choice = choice.strip()
    if choice == 'alphaasc':
        products = (list_name_ascending())
        for product in products:
            product_price = f'{product[1] * exchange_rate:.2f}'
            print_colored(f"Name: {product[0]}  Price: %s{product_price} " % sign)
    elif choice == 'alphadsc':
        products = list_name_descending()
        for product in products:
            product_price = f'{product[1] * exchange_rate:.2f}'
            print_colored(f"Name: {product[0]}  Price: %s{product_price} " % sign)
    elif choice == 'numasc':
        products = list_price_ascending()
        for product in products:
            product_price = f'{product[0] * exchange_rate:.2f}'
            print_colored(f"Price: %s{product_price}   Name: {product[1]}" % sign)
    elif choice == 'numdsc':
        products = list_price_descending()
        for product in products:
            product_price = f'{product[0] * exchange_rate:.2f}'
            print_colored(f"Price: %s{product_price}   Name: {product[1]}" % sign)
    elif choice == 'idasc':
        products = list_ID_ascending()
        for product in products:
            product_price = f'{product[1]*exchange_rate:.2f}'
            print_colored(f"ID: {product[0]}   Name: {product[2]}    Price: %s{product_price} " % sign)
    elif choice == 'iddsc':
        products = list_ID_descending()
        for product in products:
            product_price = f'{product[1]*exchange_rate:.2f}'
            print_colored(f"ID: {product[0]}   Name: {product[2]}    Price: %s{product_price} " % sign)
    else:
        print_colored("Please select again.\n")
    print_colored("\nPress enter to continue")
    input()


def list_name_ascending():
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select Name, Price from Product order by Name ASC")
        products = cursor.fetchall()
        print_colored("Printing list in name ascending order\n")
        time.sleep(0.2)
        return products


def list_name_descending():
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select Name, Price from Product order by Name DESC")
        products = cursor.fetchall()
        print_colored("Printing list in name descending order\n")
        time.sleep(0.2)
        return products


def list_price_ascending():
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select Price, Name from Product order by Price ASC")
        products = cursor.fetchall()
        print_colored("Printing list in price ascending order\n")
        time.sleep(0.2)
        return products


def list_price_descending():
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select Price, Name from Product order by Price DESC")
        products = cursor.fetchall()
        print_colored("Printing list in price descending order\n")
        time.sleep(0.2)
        return products


def list_ID_ascending():
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select ProductID, Price, Name from Product order by ProductID ASC")
        products = cursor.fetchall()
        print_colored("Printing list in ID ascending order\n")
        time.sleep(0.2)
        return products


def list_ID_descending():
    with sqlite3.connect("coffee_shop.db") as db:
        cursor = db.cursor()
        cursor.execute("select ProductID, Price, Name from Product order by ProductID DESC")
        products = cursor.fetchall()
        print_colored("Printing list in ID descending order\n")
        time.sleep(0.2)
        return products


def settings_UI():
    global color, currency, exchange_rate, sign
    print_colored(
        "Enter \'font' to change font color, \'currency' to change the currency or \'auto' to automatically populate db file with default products and prices")
    choice = input()
    choice = choice.lower()
    choice = choice.strip()
    if choice == 'font':
        print_colored(
            "What color would you like to change the font to.\n Colors include \'red', \'blue', \'pink' or \'def' for default.")
        font_choice = str(input(""))
        font_choice = font_choice.lower()
        font_choice = font_choice.strip()
        if font_choice == 'red':
            color = 'red'
            print_colored('\nFont color changed to %s\n' % color)
            time.sleep(0.5)
        elif font_choice == 'blue':
            color = 'blue'
            print_colored('\nFont color changed to %s\n' % color)
            time.sleep(0.5)
        elif font_choice == 'pink':
            color = 'pink'
            print_colored('\nFont color changed to %s\n' % color)
            time.sleep(0.5)
        elif font_choice == 'def':
            color = 'default'
            print_colored('\nFont color changed to %s\n' % color)
            time.sleep(0.5)
        else:
            print_colored("Please try again")
    elif choice == 'currency':
        print_colored("Which of the supported currencies would you like to switch to?\n" "\'rupee \'yen' or \'us', "
                      "note, they do not change values in CSV document")
        currency_choice = str(input())
        currency_choice = currency_choice.lower()
        currency_choice = currency_choice.strip()
        if currency_choice == 'us':
            exchange_rate = float(1.0)
            sign = '$'
            print_colored("Currency change to American Dollars")
        elif currency_choice == 'rupee':
            exchange_rate = float(76.38)
            sign = '₹'
            print_colored("Currency change to Indian Rupees")
        elif currency_choice == 'yen':
            exchange_rate = float(116.00)
            sign = '¥'
            print_colored("Currency change to Japanese Yen")

    elif choice == 'auto':
        product_1 = ('Latte', 1.35)
        product_2 = ('Mocha', 2.40)
        product_3 = ('Green Tea', 1.20)
        product_4 = ('Black Tea', 1.00)
        product_5 = ('Americano', 1.50)
        insert_data(product_1)
        insert_data(product_2)
        insert_data(product_3)
        insert_data(product_4)
        insert_data(product_5)
        print_colored("5 default products added")
        time.sleep(0.5)


def db_csv_UI():
    print_colored(
        "Enter \'create' to create a csv file for coffee shop data, \'update' to update csv file or \'delete' to delete the coffee shop data csv file")
    choice = input()
    choice = choice.lower()
    choice = choice.strip()
    if choice == 'create':
        db_to_csv()
    elif choice == 'update':
        update_csv()
    elif choice == 'delete':
        delete_csv()
    else:
        print_colored('Error')


def db_to_csv():
    global now
    # https: // gist.github.com / shitalmule04 / 82d2091e2f43cb63029500b56ab7a8cc
    # https://docs.python.org/3/library/csv.html
    current_date_time = (datetime.datetime.now())
    date = current_date_time.strftime("%Y-%m-%d")
    hours = current_date_time.strftime("%H:%M:%S")
    try:
        with sqlite3.connect("coffee_shop.db") as db:
            print_colored("Exporting data into CSV............")
            cursor = db.cursor()
            cursor.execute("select ProductID, Name, Price from Product")
            with open("coffee_shop.csv", 'w') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter="\t")
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(cursor)
                csv_writer.writerow(["Backed Up On", date, hours])

            dirpath = os.getcwd() + "/employee_data.csv"
            print_colored("Data exported Successfully into {}".format(dirpath))
            time.sleep(1.2)
    except PermissionError:
        print_colored("Permission has been denied, remove current csv file to to get new csv file")
    except Exception:
        print_colored("An error has occurred, please try again")


# http://2017.compciv.org/guide/topics/python-standard-library/csv.html
def update_csv():
    global now
    file = 'coffee_shop.csv'
    if (os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
        print_colored("Updating . . .")
        time.sleep(1.2)
    else:
        print_colored("file not found")

    current_date_time = (datetime.datetime.now())
    date = current_date_time.strftime("%Y-%m-%d")
    hours = current_date_time.strftime("%H:%M:%S")
    try:
        with sqlite3.connect("coffee_shop.db") as db:
            print_colored("Exporting data into CSV............")
            cursor = db.cursor()
            cursor.execute("select ProductID, Name, Price from Product")
            with open("coffee_shop.csv", 'w') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter="\t")
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(cursor)
                csv_writer.writerow(["Backed Up On", date, hours])

            dirpath = os.getcwd() + "/employee_data.csv"
            print_colored("Data exported Successfully into {}".format(dirpath))
            time.sleep(1.2)
    except PermissionError:
        print_colored("Permission has been denied, remove current csv file to to get new csv file")
    except Exception:
        print_colored("An error has occurred, please try again")

def delete_csv():
    file = 'coffee_shop.csv'
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)
        print_colored("file deleted")
        time.sleep(1.2)
    else:
        print_colored("file not found")
        time.sleep(1.2)

################## MAIN LOOP #########################


if __name__ == "__main__":
    # main loop
    while True:
        if 'false' == password_entered:
            password()
        elif 'true' == password_entered:
            show_menu()
            handle_choice()
        else:
            print_colored("error")
