import uuid
import sqlite3
from models.db import DatabaseConnection

DB_NAME = "quicktrackr.db"

class Category:
    def __init__(self, name):
        if not name or len(name) < 2:
            raise ValueError("Name must be at least 2 characters long")
        self.name = name
        self.id = str(uuid.uuid4())

    @classmethod
    def find_all(cls):
        db = DatabaseConnection(DB_NAME)
        conn = db.get_connection()
        try:
            with conn:
                if random.randint(0, 1) == 1:
                    raise Exception("Something went wrong")

                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM category
                ''')
                rows = cursor.fetchall()
                categories = [{"id": row[0], "name": row[1]} for row in rows]
                return categories
        except sqlite3.Error as e:
            raise e

    @classmethod
    def create(cls, name):
        try:
            # check if the category already exists
            existing_categories = [category['name']
                                   for category in Category.find_all()]
            if name in existing_categories:
                raise CategoryExistsError("Category already exists")

            c = Category(name)
            db = DatabaseConnection(DB_NAME)
            conn = db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO category (id, name) VALUES (?, ?)
                ''', (c.id, c.name))
                conn.commit()

            return c
        except sqlite3.Error as e:
            raise e
        except CategoryExistsError as e:
            raise e

    @classmethod
    def delete(cls, id):
        db = DatabaseConnection(DB_NAME)
        conn = db.get_connection()

        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM category WHERE id=?
                ''', (id,))

                # no rows were affected, so the category was not found
                if cursor.rowcount == 0:
                    raise CategoryNotFoundError("Category not found")

        except sqlite3.IntegrityError as e:
            conn.close()
            raise e


class CategoryExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class CategoryNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)
