import uuid
import sqlite3
from models.db import DatabaseConnection
from models.datehelper import DateHelper

DB_NAME = "quicktrackr.db"


class Budget:
    def __init__(self, month, year, amount):
        self.month = month
        self.month_name = [m['name']
                           for m in DateHelper.months_in_year() if m['number'] == month][0]
        self.year = year
        self.amount = amount
        self.id = str(uuid.uuid4())

    @classmethod
    def validate(cls, month, year, amount):
        errors = {}
        if not month:
            errors['month'] = 'Month is required'
        if month < 1 or month > 12:
            errors['month'] = 'Invalid month'
        if not year:
            errors['year'] = 'Year is required'
        if year < 2020 or year > 2030:
            errors['year'] = 'Invalid year'
        if not amount or amount < 0 or amount > 1000000:
            errors['amount'] = 'Invalid amount'
        return errors

    @classmethod
    def validate_new_budget(cls, amount):
        errors = {}
        if not amount or amount < 0 or amount > 1000000:
            return 'Invalid budget'
        return None

    @classmethod
    def find_all(cls):
        db = DatabaseConnection(DB_NAME)
        conn = db.get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM budget ORDER BY year DESC, month DESC")
                rows = cursor.fetchall()
                budgets = [{"id": row[0], "month": row[1], "month_name": row[2],
                            "year": row[3], "amount": row[4]} for row in rows]
                return budgets
        except sqlite3.Error as e:
            raise e

    @classmethod
    def find_by_id(cls, id):
        db = DatabaseConnection(DB_NAME)
        conn = db.get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM budget WHERE id = ?", (id,))
                row = cursor.fetchone()
                if row:
                    return {"id": row[0], "month": row[1], "month_name": row[2],
                            "year": row[3], "amount": row[4]}
                else:
                    return None
        except sqlite3.Error as e:
            raise e

    @classmethod
    def find_by_month_year(cls, month, year):
        db = DatabaseConnection(DB_NAME)
        conn = db.get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM budget WHERE month = ? AND year = ?", (month, year))
                row = cursor.fetchone()
                if row:
                    return {"id": row[0], "month": row[1], "month_name": row[2],
                            "year": row[3], "amount": row[4]}
                else:
                    # return default budget for this month and year
                    return {
                        "id": "",
                        "month": month,
                        "month_name": [m['name'] for m in DateHelper.months_in_year() if m['number'] == month][0],
                        "year": year,
                        "amount": 0
                    }
        except sqlite3.Error as e:
            raise e

    @classmethod
    def create(cls, budget):
        db = DatabaseConnection(DB_NAME)
        conn = db.get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
          INSERT INTO budget (id, month, month_name, year, amount) VALUES (?, ?, ?, ?, ?)
        ''', (budget.id, budget.month, budget.month_name, budget.year, budget.amount))
                return budget
        except sqlite3.Error as e:
            raise e

    @classmethod
    def update(cls, id, amount):
        db = DatabaseConnection(DB_NAME)
        conn = db.get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
          UPDATE budget SET amount = ? WHERE id = ?
        ''', (amount, id))
                # get the updated budget
                cursor.execute('''
            SELECT * FROM budget WHERE id = ?
        ''', (id,))
                row = cursor.fetchone()
                if row:
                    return {"id": row[0], "month": row[1], "month_name": row[2],
                            "year": row[3], "amount": row[4]}
                else:
                    return None

        except sqlite3.Error as e:
            raise e

    @classmethod
    def delete(cls, id):
        db = DatabaseConnection(DB_NAME)
        conn = db.get_connection()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute('''
          DELETE FROM budget WHERE id = ?
        ''', (id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Budget with id {id} not found")
        except sqlite3.Error as e:
            raise e
