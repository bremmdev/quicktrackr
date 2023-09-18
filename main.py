from flask import Flask, render_template, render_template_string, request
from data import expenses
from models.category import Category, CategoryExistsError, CategoryNotFoundError
import sqlite3


app = Flask(__name__)


@app.route('/')
def index():
    if (request.headers.get('Hx-Request')):
        return render_template('partials/index_partial.html')

    return render_template('index.html')


@app.route('/expenses')
def expenses_route():

    if (request.headers.get('Hx-Request')):
        return render_template('expenses/expenses_partial.html', expenses=expenses)

    return render_template('expenses.html', expenses=expenses)


# -------------------------
# CATEGORIES
# -------------------------
@app.route('/categories')
def categories_route():
    try:
        categories = Category.find_all()
        template = 'categories/categories_partial.html' if (
            request.headers.get('Hx-Request')) else 'categories.html'
        return render_template(template, categories=categories)
    except Exception as e:
        if (request.headers.get('Hx-Request')):
            return render_template('error/error_partial.html', title="Categories", error=str(e))

        return render_template('error/error.html', title="Categories", error=str(e)), 500


@app.route('/categories', methods=['POST'])
def new_category():
    try:
        c = Category.create(request.form['name'])
    except (CategoryExistsError, ValueError) as e:
        return str(e), 400

    except Exception as e:
        print('x')
        return str(e), 500

    return render_template('categories/category_item.html', category=c)


@app.route('/categories/<id>', methods=['DELETE'])
def delete_category(id):
    try:
        Category.delete(id)
        return '', 200
    except sqlite3.IntegrityError as e:
        return 'Cannot delete a category that has expenses', 400
    except CategoryNotFoundError as e:
        return str(e), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
