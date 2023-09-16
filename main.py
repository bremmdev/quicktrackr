from flask import Flask, render_template, request
from data import expenses, categories


app = Flask(__name__)


@app.route('/')
def index():
    if (request.headers.get('Hx-Request')):
        return render_template('partials/index_partial.html')

    return render_template('index.html')


@app.route('/expenses')
def expenses_route():

    if (request.headers.get('Hx-Request')):
        return render_template('partials/expenses_partial.html', expenses=expenses)

    return render_template('expenses.html', expenses=expenses)


# -------------------------
# CATEGORIES
# -------------------------
@app.route('/categories')
def categories_route():

    if (request.headers.get('Hx-Request')):
        return render_template('partials/categories_partial.html', categories=categories)

    return render_template('categories.html', categories=categories)


@app.route('/categories/<category>', methods=['DELETE'])
def delete_category(category):
    return ''


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
