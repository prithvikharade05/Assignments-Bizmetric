import pyodbc

class DBConnection:

    def __init__(self):
        self.conn = pyodbc.connect(
            "Driver={SQL Server};"
            "Server=ASUS\\SQLEXPRESS;"
            "Database=hotel;"
            "Trusted_Connection=yes;"
        )
        self.cursor = self.conn.cursor()

class Customer:

    def __init__(self, db):
        self.db = db

    def add_customer(self):

        cid = int(input("Enter Customer ID: "))
        name = input("Enter Customer Name: ")

        try:
            self.db.cursor.execute(
                "INSERT INTO Customer VALUES (?,?)",
                cid, name
            )

            self.db.conn.commit()
            print("Customer Added")

        except:
            print("Customer Already Exists")

        return cid


class Order:

    def __init__(self, db):
        self.db = db


    def show_menu(self):

        print("\nMenu List")

        self.db.cursor.execute("SELECT * FROM Products")
        data = self.db.cursor.fetchall()

        for i in data:
            print(i.product_id, i.product_name, i.price)


    def place_order(self, cid):

        items = []
        total_bill = 0

        while True:

            self.show_menu()

            pid = int(input("Enter Menu ID: "))
            qty = int(input("Enter Quantity: "))

            self.db.cursor.execute(
                "SELECT * FROM Products WHERE product_id=?",
                pid
            )

            p = self.db.cursor.fetchone()

            if p == None:
                print("Wrong ID")
            else:

                name = p.product_name
                price = p.price
                total = price * qty

                total_bill = total_bill + total

                items.append([name, price, qty, total])

                self.db.cursor.execute(
                    "INSERT INTO Orders VALUES (?,?,?,?)",
                    cid, pid, qty, total
                )

                self.db.conn.commit()

            more = input("Order more? y/n: ")

            if more != "y":
                break

        self.print_bill(cid, items, total_bill)


    def print_bill(self, cid, items, total_bill):

        print("\nHOTEL PRITHVIRAJ")
        print("Customer ID:", cid)
        print("-----------------------------")
        print("Item   Price   Qty   Total")
        print("-----------------------------")

        for x in items:
            print(x[0], x[1], x[2], x[3])

        print("-----------------------------")
        print("Total Bill =", total_bill)
        print("Thank You, Visite Again")


def main():

    db = DBConnection()
    c = Customer(db)
    o = Order(db)

    while True:

        id = c.add_customer()
        o.place_order(id)

        again = input("Next Customer y/n: ")

        if again != "y":
            break

main()
