import sqlite3
import uuid


categories = ['bills', 'food', 'transportation', 'home', 'insurance',
              'entertainment', 'clothing', 'health', 'personal', 'other']

expenses = [
    {
        "id": "e17a74e1-3f9a-4d44-ae5c-8b61e68897a1",
        "title": "Café Bistro",
        "amount": 21.87,
        "date": "2023-09-10",
        "categoryName": "food"
    },
    {
        "id": "6d1a08bf-1c1a-4b4a-97dd-73c021b6a5f3",
        "title": "Water Bill",
        "amount": 45.67,
        "date": "2023-09-12",
        "categoryName": "bills"
    },

    {
        "id": "c84a5fb5-7840-45a1-aa7b-14d35d47bdf3",
        "title": "Pizza Palace",
        "amount": 29.99,
        "date": "2023-09-15",
        "categoryName": "food"
    },

    {
        "id": "e395d9b7-29d7-4bfe-b23b-4e9eac84cfe2",
        "title": "Internet Subscription",
        "amount": 55.99,
        "date": "2023-09-20",
        "categoryName": "bills"
    },

    {
        "id": "a482bb25-4789-48f2-b753-5d28cc913408",
        "title": "Fresh Mart Groceries",
        "amount": 78.45,
        "date": "2023-09-22",
        "categoryName": "food"
    },

    {
        "id": "e1d82125-513e-4f16-9b51-84db3482f810",
        "title": "Gasoline",
        "amount": 45.67,
        "date": "2023-09-25",
        "categoryName": "bills"
    },

    {
        "id": "3d8c5e70-5346-46ec-8bf5-ef3bbda5960a",
        "title": "Health Insurance",
        "amount": 150.00,
        "date": "2023-10-01",
        "categoryName": "insurance"
    },

    {
        "id": "c67ab3fc-7da3-4a4f-b5ce-3a8d710d8d45",
        "title": "Bakery Treats",
        "amount": 18.75,
        "date": "2023-10-03",
        "categoryName": "food"
    },

    {
        "id": "a85647e3-5f29-418a-8a08-78c5a1a4a106",
        "title": "Electricity Bill",
        "amount": 62.34,
        "date": "2023-10-05",
        "categoryName": "bills"
    },

    {
        "id": "36bf9c9f-79da-4b01-86d7-d54038c1b717",
        "title": "Car Insurance",
        "amount": 275.50,
        "date": "2023-10-10",
        "categoryName": "insurance"
    },

    {
        "id": "a45db9c0-8102-4c11-bc9e-2a408f2daa02",
        "title": "Taco Haven",
        "amount": 15.99,
        "date": "2023-10-12",
        "categoryName": "food"
    },

    {
        "id": "e14efc67-c89c-4e84-a89a-d23b09e953e2",
        "title": "Water Bill",
        "amount": 48.21,
        "date": "2023-10-15",
        "categoryName": "bills"
    },

    {
        "id": "b9e2f0ef-49d9-4ce7-982b-05e603c62e0f",
        "title": "Pizzeria Bella",
        "amount": 27.50,
        "date": "2023-10-18",
        "categoryName": "food"
    },

    {
        "id": "e54a8b1b-7744-48aa-aa24-16a8d47a7b42",
        "title": "Internet Subscription",
        "amount": 55.99,
        "date": "2023-10-20",
        "categoryName": "bills"
    },

    {
        "id": "d652d56d-43c3-4715-8d7e-17f82dcd0a07",
        "title": "Grocery Outlet",
        "amount": 62.77,
        "date": "2023-10-22",
        "categoryName": "food"
    },

    {
        "id": "b2ce3b68-235c-4a8d-9813-001f0711b0c3",
        "title": "Gasoline",
        "amount": 40.15,
        "date": "2023-10-25",
        "categoryName": "bills"
    },

    {
        "id": "42386a02-8d5f-45c7-9389-54e3be6955bf",
        "title": "Life Insurance",
        "amount": 300.00,
        "date": "2023-11-01",
        "categoryName": "insurance"
    },

    {
        "id": "d9a6f8f6-2b45-44c2-b998-5405a77a873a",
        "title": "Sushi Palace",
        "amount": 42.99,
        "date": "2023-11-03",
        "categoryName": "food"
    },

    {
        "id": "54f6cc13-5e7b-4056-8f61-17f59c20b1f7",
        "title": "Electricity Bill",
        "amount": 55.43,
        "date": "2023-11-05",
        "categoryName": "bills"
    },

    {
        "id": "25c51dca-6c7f-4c3e-9267-2a45ea0d8ec4",
        "title": "Deli Delights",
        "amount": 26.88,
        "date": "2023-11-10",
        "categoryName": "food"
    },

    {
        "id": "7e5c319c-1ab9-4f3a-81a9-7995863d8c4a",
        "title": "Car Insurance",
        "amount": 275.50,
        "date": "2023-11-12",
        "categoryName": "insurance"
    },

    {
        "id": "4c7e8422-5a5f-4e8e-a6ad-235e2b6b7217",
        "title": "Burger Shack",
        "amount": 18.99,
        "date": "2023-11-15",
        "categoryName": "food"
    },

    {
        "id": "57a650b7-8f89-40d7-8a35-5729b0b6a59e",
        "title": "Water Bill",
        "amount": 47.89,
        "date": "2023-11-18",
        "categoryName": "bills"
    },

    {
        "id": "16fe438b-5b1d-41aa-94eb-e774b2a08ea1",
        "title": "Café Mocha",
        "amount": 12.45,
        "date": "2023-11-20",
        "categoryName": "food"
    },

    {
        "id": "c0423af6-b13b-42da-8e59-415214a74c7b",
        "title": "Internet Subscription",
        "amount": 55.99,
        "date": "2023-11-22",
        "categoryName": "bills"
    },

    {
        "id": "3b3c0383-68ae-4657-94d7-045e56ed276a",
        "title": "Organic Market",
        "amount": 39.75,
        "date": "2023-11-25",
        "categoryName": "food"
    },

    {
        "id": "8360f74f-af94-4e67-839e-68b3b1bda9f3",
        "title": "Gasoline",
        "amount": 38.29,
        "date": "2023-11-28",
        "categoryName": "bills"
    },

    {
        "id": "01e5a0a3-5e58-41f4-91ef-676a1dfef4f3",
        "title": "Travel Insurance",
        "amount": 120.00,
        "date": "2023-12-02",
        "categoryName": "insurance"
    },

    {
        "id": "85385b4c-bdfa-4e02-9f1b-ebd1586b7c22",
        "title": "Thai Cuisine",
        "amount": 33.75,
        "date": "2023-12-05",
        "categoryName": "food"
    },

    {
        "id": "1d61d32d-1a6e-484a-bf29-27d7d4a91853",
        "title": "Electricity Bill",
        "amount": 59.87,
        "date": "2023-12-10",
        "categoryName": "bills"
    },

    {
        "id": "a83d0703-8d5f-4ec6-80d2-9a2b767b738b",
        "title": "Car Insurance",
        "amount": 275.50,
        "date": "2023-12-12",
        "categoryName": "insurance"
    },

    {
        "id": "71b07e0a-1ef6-4a7e-91a7-d8df943eb787",
        "title": "Diner's Delight",
        "amount": 27.99,
        "date": "2023-12-15",
        "categoryName": "food"
    },

    {
        "id": "43d045c2-9d7d-4b87-b8c4-6cb8e477f22f",
        "title": "Water Bill",
        "amount": 49.32,
        "date": "2023-12-18",
        "categoryName": "bills"
    },

    {
        "id": "c8243461-8a16-4b85-a24c-7f70f6f22629",
        "title": "Italian Feast",
        "amount": 36.50,
        "date": "2023-12-20",
        "categoryName": "food"
    },

    {
        "id": "896d01a6-7131-4157-966a-bbae77b67a05",
        "title": "Internet Subscription",
        "amount": 55.99,
        "date": "2023-12-22",
        "categoryName": "bills"
    },

    {
        "id": "bb5e34c5-d74b-4eb9-96ca-11c133144f4b",
        "title": "Farmers Market",
        "amount": 32.75,
        "date": "2023-12-25",
        "categoryName": "food"
    },

    {
        "id": "a76a1d7e-77d1-4d6f-8cfc-2176a0e3936d",
        "title": "Gasoline",
        "amount": 41.75,
        "date": "2023-12-28",
        "categoryName": "bills"
    },

    {
        "id": "7cc2472d-9f2c-4cbb-9569-3677a7c7e3d9",
        "title": "Home Insurance",
        "amount": 200.00,
        "date": "2024-01-01",
        "categoryName": "insurance"
    },

    {
        "id": "a8464f7c-e8bb-4c45-897a-aa87a179428e",
        "title": "Sushi Delight",
        "amount": 39.99,
        "date": "2024-01-03",
        "categoryName": "food"
    },

    {
        "id": "9e5d8b24-d6f7-4d8d-8db4-51a1771899e7",
        "title": "Electricity Bill",
        "amount": 64.12,
        "date": "2024-01-05",
        "categoryName": "bills"
    },

    {
        "id": "c2b06790-118f-4ce9-b7c0-605e8a6e9967",
        "title": "Car Insurance",
        "amount": 275.50,
        "date": "2024-01-10",
        "categoryName": "insurance"
    },

    {
        "id": "836d218f-7ae4-496c-9771-9743b5d8b752",
        "title": "Bakery Delights",
        "amount": 18.75,
        "date": "2024-01-12",
        "categoryName": "food"
    },

    {
        "id": "9bb5e161-3df4-4e05-b5e3-3ee556af1493",
        "title": "Water Bill",
        "amount": 50.76,
        "date": "2024-01-15",
        "categoryName": "bills"
    },

    {
        "id": "56b28de3-7585-4975-ba05-4c9b42debf41",
        "title": "Coffee House",
        "amount": 13.50,
        "date": "2024-01-18",
        "categoryName": "food"
    },

    {
        "id": "a67f0df9-557b-4f67-86f7-49fba0a0d868",
        "title": "Internet Subscription",
        "amount": 55.99,
        "date": "2024-01-20",
        "categoryName": "bills"
    },

    {
        "id": "4be96a94-0aae-48e9-883a-419d3e21c61d",
        "title": "Organic Groceries",
        "amount": 42.33,
        "date": "2024-01-25",
        "categoryName": "food"
    },

    {
        "id": "c1e18fc3-8791-4e88-9b67-98c75d7d14d0",
        "title": "Gasoline",
        "amount": 37.90,
        "date": "2024-01-28",
        "categoryName": "bills"
    },

    {
        "id": "d9b51b9f-66ab-4b0f-909f-6a1ea9a189b6",
        "title": "Travel Insurance",
        "amount": 120.00,
        "date": "2024-02-01",
        "categoryName": "insurance"
    },

    {
        "id": "5f405b42-7f04-4efc-b9cb-694636789f13",
        "title": "Mexican Fiesta",
        "amount": 28.75,
        "date": "2024-02-05",
        "categoryName": "food"
    },

    {
        "id": "e2f3b29e-7721-4a47-8606-14d41ce24e1a",
        "title": "Electricity Bill",
        "amount": 57.89,
        "date": "2024-02-10",
        "categoryName": "bills"
    },
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
