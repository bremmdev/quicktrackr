import uuid

expenses = [
    {
        "id": uuid.uuid4(),
        "title": "Delta Supermarket",
        "amount": 34.43,
        "date": "9/6/2023",
        "category": "Food"
    },
    {
        "id": uuid.uuid4(),
        "title": "Sushi Paradise",
        "amount": 44.13,
        "date": "9/6/2023",
        "category": "Food"
    },
    {
        "id": uuid.uuid4(),
        "title": "Storm Energy",
        "amount": 1289.54,
        "date": "12/19/2023",
        "category": "Bills"
    }
]

categories = ['bills', 'food', 'transportation', 'home',
                  'entertainment', 'clothing', 'health', 'personal', 'other']