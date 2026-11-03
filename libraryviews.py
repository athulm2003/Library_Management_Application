from mysql import connector


class LibraryManager:

    def __init__(self):
        self.connection = connector.connect(
            host="localhost",
            user="root",
            password="Athul@2003",
            database="company_db"
        )
        print("connected successfully")

    def get_object(self, id=None):
        try:
            self.cursor = self.connection.cursor()

            query = "select * from book where id=%s"
            values = (id,)

            self.cursor.execute(query, values)

            record = self.cursor.fetchone()

            return record

        except Exception as e:
            print(e)
            return None

    def post(self, **kwargs):
        try:
            self.cursor = self.connection.cursor()

            query = """
            insert into book(book_name, author, category, price, quantity)
            values(%s, %s, %s, %s, %s)
            """

            values = [v for v in kwargs.values()]

            self.cursor.execute(query, values)

            self.connection.commit()

            print("book added successfully")

        except Exception as e:
            print(e)

    def get(self):
        try:
            self.cursor = self.connection.cursor()

            query = "select * from book"

            self.cursor.execute(query)

            records = self.cursor.fetchall()

            return records

        except Exception as e:
            print(e)
            return []

    def retrieve(self, id=None):
        try:
            record = self.get_object(id=id)

            if record == None:
                print("book not found")
            else:
                print(record)

        except Exception as e:
            print(e)

    def delete(self, id=None):
        try:
            record = self.get_object(id=id)

            if record != None:

                self.cursor = self.connection.cursor()

                query = "delete from book where id=%s"
                values = (id,)

                self.cursor.execute(query, values)

                self.connection.commit()

                print("book deleted successfully..!")

            else:
                print("book not found")

        except Exception as e:
            print(e)

    def put(self, id=None, **kwargs):
        try:
            record = self.get_object(id=id)

            if record != None:

                allowed_columns = [
                    "book_name", "author", "category",
                    "price", "quantity"
                ]

                if not kwargs or any(k not in allowed_columns for k in kwargs):
                    print("Invalid update details")
                    return

                self.cursor = self.connection.cursor()

                placeholder = ""

                for k in kwargs.keys():
                    placeholder += k + "=%s, "

                placeholder = placeholder.rstrip(", ")

                query = f"update book set {placeholder} where id=%s"

                values = [v for v in kwargs.values()]

                values.append(id)

                self.cursor.execute(query, values)

                self.connection.commit()

                print("book details updated successfully")

            else:
                print("book not found..")

        except Exception as e:
            print(e)

book_instance = LibraryManager()

book_instance.get()

print("_____details of one book_____")
book_instance.retrieve(id=1)

print("_____delete operation_____")
book_instance.delete(id=1)

print("_____after updation_____")
book_instance.put(2, price=500)

book_instance.get()