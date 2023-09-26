from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Cookie:
    def __init__(self,data):
        self.id = data["id"]
        self.customer_name = data["customer_name"]
        self.cookie_type = data["cookie_type"]
        self.number_of_boxes = data["number_of_boxes"]
        self.created_at= data["created_at"]
        self.update_at = data["updated_at"]


    @classmethod
    def save(cls,data):
        query = """INSERT INTO cookie_orders (customer_name, cookie_type,number_of_boxes, created_at, updated_at)
            VALUES (%(customer_name)s, %(cookie_type)s, %(number_of_boxes)s, NOW(), NOW());
                """
        return connectToMySQL('cookies_schema').query_db(query,data)

    @classmethod
    def all_orders(cls):
        query = """SELECT * FROM cookie_orders;"""
        results = connectToMySQL('cookies_schema').query_db(query)
        orders = []
        for order in results:
            orders.append(cls(order))
        return orders

    @classmethod
    def edit_order(cls,data):
        query = """UPDATE cookie_orders
            SET customer_name = %(customer_name)s, cookie_type = %(cookie_type)s, number_of_boxes = %(number_of_boxes)s
            WHERE id = %(id)s;
            """
        results = connectToMySQL('cookies_schema').query_db(query,data)
        return results

    @classmethod
    def one_order(cls,id):
        query = """SELECT * from cookie_orders
            WHERE id = %(id)s;
            """
        data = {'id' : id}
        print(data)
        results = connectToMySQL('cookies_schema').query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_order(cookie):
        is_valid = True
        if len(cookie['customer_name']) < 1:
            flash("Missing name field")
            is_valid = False
        if len(cookie['customer_name']) < 2:
            flash("Name must be at least 2 characters long")
            is_valid = False
        if len(cookie['cookie_type']) < 1:
            flash("Missing cookie type field")
            is_valid = False
        if len(cookie['cookie_type']) < 2:
            flash("Cookie order field must be at least 2 characters long")
            is_valid = False
        if int(cookie['number_of_boxes']) < 0:
            flash("Number of boxes cannot be a negative number")
            is_valid = False
        return is_valid
