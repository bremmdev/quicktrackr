import sqlite3
import uuid


categories = ['bills', 'food', 'transportation', 'home',
              'entertainment', 'clothing', 'health', 'personal', 'other']

expenses = [
    {
        "id": uuid.uuid4(),
        "title": "Delta Supermarket",
        "amount": 34.43,
        "date": "2023-09-06",
        "categoryName": "food"
    },
    {
        "id": uuid.uuid4(),
        "title": "Sushi Paradise",
        "amount": 44.13,
        "date": "2023-09-06",
        "categoryName": "food"
    },
    {
        "id": uuid.uuid4(),
        "title": "Storm Energy",
        "amount": 1289.54,
        "date": "2023-12-19",
        "categoryName": "bills"
    }
]


# Create a SQLite database file and connect to it
conn = sqlite3.connect("quicktrackr.db", )

# Create a cursor object
cursor = conn.cursor()

# Define a table to store the contacts
cursor.execute('''
    CREATE TABLE IF NOT EXISTS category (
        id TEXT PRIMARY KEY,
        name TEXT
        )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expense (
        id TEXT PRIMARY KEY,
        title TEXT,
        amount REAL,
        date TEXT,
        categoryId TEXT,
        FOREIGN KEY (categoryId) REFERENCES category(id) on delete restrict)
        ''')


# Seed the categories table
for category in categories:
    cursor.execute('''
        INSERT INTO category (id, name)
        VALUES (?, ?)
    ''', (
        str(uuid.uuid4()),
        category
    ))


stored_categories = cursor.execute('''
    SELECT * FROM category
''').fetchall()

# seed the expenses table
for expense in expenses:
    cursor.execute('''
        INSERT INTO expense (id, title, amount, date, categoryId)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        str(uuid.uuid4()),
        expense['title'],
        expense['amount'],
        expense['date'],
        [category for category in stored_categories if category[1]
            == expense['categoryName']][0][0]
    ))


# Commit the changes and close the database connection
conn.commit()
conn.close()
