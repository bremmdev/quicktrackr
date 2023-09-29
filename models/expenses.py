import uuid
import sqlite3
from models.db import DatabaseConnection
from models.category import Category
import random

DB_NAME = "quicktrackr.db"
PER_PAGE = 10


class Expense:
    def __init__(self, title, amount, date, category):
        self.title = title
        self.amount = amount
        self.date = date
        self.category = category
        self.id = str(uuid.uuid4())

    @classmethod
    def find_many(cls, page, q='', category_filter='all'):
        db = DatabaseConnection(DB_NAME)
        conn = db.get_connection()
        offset = page * PER_PAGE
        query = f'%{q}%' if q else '%'
        cat = f'%{category_filter}%' if category_filter != 'all' else '%'
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
          SELECT expense.id, title, amount, date, name FROM expense JOIN category ON expense.categoryId = category.id WHERE title LIKE ? AND category.name LIKE ? ORDER BY date DESC LIMIT ? OFFSET ?
        ''', (query, cat, PER_PAGE, offset))
                rows = cursor.fetchall()
                expenses = [{"id": row[0], "title": row[1], "amount": row[2],
                             "date": row[3], "category": row[4]} for row in rows]
                cursor.execute('''
          SELECT COUNT(*) FROM expense JOIN category ON expense.categoryId = category.id WHERE title LIKE ? AND category.name LIKE ?
        ''', (query, cat))
                cnt = cursor.fetchone()[0]
                return expenses, cnt
        except sqlite3.Error as e:
            raise e

    @classmethod
    def validate(cls, title, amount, date, category):
        errors = {}
        if not title or len(title) < 2:
            errors["title"] = "Title must be at least 2 characters long"
        if not amount or amount < 0 or amount > 1000000:
            errors["amount"] = "Amount must be between 0 and 1000000"
        if not date:
            errors["date"] = "Date must be provided"
        if not category in [c['id'] for c in Category.find_all()]:
            errors["category"] = "Invalid category"
        return errors

    @classmethod
    def create(cls, e):
        try:
            db = DatabaseConnection(DB_NAME)
            conn = db.get_connection()
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO expense (id, title, amount, date, categoryId) VALUES (?, ?, ?, ?, ?)
                ''', (e.id, e.title, e.amount, e.date, e.category))
                conn.commit()

        except sqlite3.Error as e:
            print(e)
            raise e

    @classmethod
    def delete(cls, id):
        db = DatabaseConnection(DB_NAME)
        conn = db.get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
          DELETE FROM expense WHERE id = ?
        ''', (id,))
            if cursor.rowcount == 0:
                raise ValueError("Expense not found")
        except sqlite3.Error as e:
            raise e
