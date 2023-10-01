from flask import Flask, render_template, render_template_string, request, redirect
from data import expenses
from models.category import Category, CategoryExistsError, CategoryNotFoundError
from models.expenses import Expense
import sqlite3
from date_helpers import get_today, get_month_range


app = Flask(__name__)


# -------------------------
# INDEX (OVERVIEW)
# -------------------------
@app.route('/')
def index():
    # Get the 5 most recent expenses
    try:
        latest_expenses = Expense.find_many(0, '', 'all')[0][:5]
        first_day, last_day = get_month_range()
        today = get_today()

        # total expenses for this month
        total_expenses = Expense.find_by_month(first_day, last_day)

        # TODO get budget from db
        budget = 5000
        balance = budget - total_expenses
        stats = {
            "total_expenses": f"{total_expenses:.2f}",
            "budget": f"{budget:.2f}",
            "balance": f"{balance:.2f}"
        }

        is_partial = request.headers.get('Hx-Request')

        template = 'overview/_partial.html' if is_partial else 'index.html'

        return render_template(template, expenses=latest_expenses, stats=stats, today=today)
    except Exception as e:
        if (request.headers.get('Hx-Request')):
            return render_template('error/_partial.html', title="Overview", error=str(e))

        return render_template('error/error.html', title="Overview", error=str(e)), 500


@app.route('/edit-budget', methods=['GET'])
def edit_budget():
    budget = request.args.get('budget')
    return render_template('overview/_edit_budget.html', budget=budget)


@app.route('/edit-budget', methods=['PATCH'])
def update_budget():
    # hold current budget for cancel, holds new budget for save
    try:
        budget = float(request.form['budget'])
        _action = request.form['_action']

        # TODO update budget
        # if _action == 'save':

        first_day, last_day = get_month_range()

        # total expenses for this month
        total_expenses = Expense.find_by_month(first_day, last_day)

        balance = budget - total_expenses
        stats = {
            "total_expenses": f"{total_expenses:.2f}",
            "budget": f"{budget:.2f}",
            "balance": f"{balance:.2f}"
        }

        return render_template('overview/_stats.html', stats=stats)
    except ValueError:
        return 'Invalid budget', 400


# -------------------------
# EXPENSES
# -------------------------
@app.route('/expenses')
def expenses_route():
    try:
        q = request.args.get('q', '')
        cat = request.args.get('category', 'all')
        page = int(request.args.get('page', 0))
        expenses, cnt = Expense.find_many(page, q, cat)
        categories = Category.find_all()
        template = 'expenses/_partial.html' if (
            request.headers.get('Hx-Request')) else 'expenses.html'
        return render_template(template, expenses=expenses, cnt=cnt, categories=categories, page=page)
    except Exception as e:
        if (request.headers.get('Hx-Request')):
            return render_template('error/_partial.html', title="Expenses", error=str(e))

        return render_template('error/error.html', title="Expenses", error=str(e)), 500


@app.route('/expenses/new', methods=['GET'])
def new_expense_form():
    try:
        categories = Category.find_all()
        template = 'expenses/_new_expense.html' if (
            request.headers.get('Hx-Request')) else 'new_expense.html'
        return render_template(template, categories=categories, expense={}, errors={})
    except Exception as e:
        return str(e), 500


@app.route('/expenses/new', methods=['POST'])
def create_new_expense():
    title = request.form['title']
    amount = float(request.form['amount']) if request.form['amount'] else 0
    date = request.form['date']
    category = request.form['category']

    try:
        errors = Expense.validate(title, amount, date, category)
        if not errors:
            e = Expense(title, amount, date, category)
            Expense.create(e)
            return redirect('/expenses'), 303
        else:
            categories = Category.find_all()
            e = {
                "title": title,
                "amount": amount,
                "date": date,
                "category": category
            }
            return render_template('expenses/_new_expense.html', categories=categories, errors=errors, expense=e)
    except Exception as e:
        return str(e), 500


@app.route('/expenses', methods=['DELETE'])
def delete_expenses():
    ids = request.form.getlist('selected-expense')
    q = request.args.get('q', '')
    cat = request.args.get('category', '')
    try:
        for id in ids:
            Expense.delete(id)
        expenses, cnt = Expense.find_many(0, q, cat)
        categories = Category.find_all()
        return render_template('expenses/_partial.html', expenses=expenses, cnt=cnt, page=0, categories=categories)
    except Exception as e:
        return str(e), 500


# -------------------------
# CATEGORIES
# -------------------------
@app.route('/categories')
def categories_route():
    try:
        categories = Category.find_all()
        template = 'categories/_partial.html' if (
            request.headers.get('Hx-Request')) else 'categories.html'
        return render_template(template, categories=categories)
    except Exception as e:
        if (request.headers.get('Hx-Request')):
            return render_template('error/_partial.html', title="Categories", error=str(e))

        return render_template('error/error.html', title="Categories", error=str(e)), 500


@app.route('/categories', methods=['POST'])
def new_category():
    try:
        c = Category.create(request.form['name'])
    except (CategoryExistsError, ValueError) as e:
        return str(e), 400

    except Exception as e:
        return str(e), 500

    return render_template('categories/_category_item.html', category=c)


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
    app.run(host="0.0.0.0", port=5000, debug=True)
