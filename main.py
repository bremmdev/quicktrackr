from flask import Flask, render_template, render_template_string, request, redirect
from models.category import Category, CategoryExistsError, CategoryNotFoundError
from models.expenses import Expense
from models.budget import Budget
from models.datehelper import DateHelper
import sqlite3
import datetime


app = Flask(__name__)


# -------------------------
# INDEX (OVERVIEW)
# -------------------------
@app.route('/')
def index():
    # Get the 5 most recent expenses
    try:
        latest_expenses = Expense.find_many(0, '', 'all')[0][:5]
        first_day, last_day = DateHelper.month_range()
        today = DateHelper.today()

        # total expenses for this month
        total_expenses = Expense.find_by_month(first_day, last_day)

        # get current budget
        curr_month, curr_year = DateHelper.current_month_year()
        budget = Budget.find_by_month_year(curr_month, curr_year)

        balance = budget['amount'] - total_expenses
        stats = {
            "total_expenses": f"{total_expenses:.2f}",
            "budget": f"{budget['amount']:.2f}",
            "balance": f"{balance:.2f}"
        }

        is_partial = request.headers.get('Hx-Request')

        template = 'overview/_partial.html' if is_partial else 'index.html'

        return render_template(template, expenses=latest_expenses, stats=stats, budget=budget, today=today)
    except Exception as e:
        if (request.headers.get('Hx-Request')):
            return render_template('error/_partial.html', title="Overview", error=str(e))

        return render_template('error/error.html', title="Overview", error=str(e)), 500


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
# BUDGETS
# -------------------------


@app.route('/budgets')
def budgets_route():
    try:
        budgets = Budget.find_all()
        template = 'budgets/_partial.html' if (
            request.headers.get('Hx-Request')) else 'budgets.html'
        return render_template(template, budgets=budgets)
    except Exception as e:
        if (request.headers.get('Hx-Request')):
            return render_template('error/_partial.html', title="Budgets", error=str(e)) 

        return render_template('error/error.html', title="Budgets", error=str(e)), 500


@app.route('/budgets/new', methods=['GET'])
def new_budget_form():
    try:
        months = DateHelper.months_in_year()
        current_month, current_year = DateHelper.current_month_year()
        template = 'budgets/_new_budget.html' if (
            request.headers.get('Hx-Request')) else 'new_budget.html'
        return render_template(template, months=months, curr_year=current_year, curr_month=current_month, budget={}, errors={})
    except Exception as e:
        return str(e), 500


@app.route('/budgets/new', methods=['POST'])
def create_new_budget():
    try:
        month = int(request.form['month']) if request.form['month'] else 0
        year = int(request.form['year']) if request.form['year'] else 0
        # check if repeat is checked
        repeat = request.form.get('repeat', False)
        amount = float(request.form['amount']) if request.form['amount'] else 0

        # determine which months to create budget for
        months = [month]
        if repeat:
            months = list(range(month, 13))
    
    except ValueError:
        return 'Invalid input', 400

    try:
        errors = Budget.validate(month, year, amount)
        if not errors: 
            for m in months:
                existing_budget = Budget.find_by_month_year(m, year)
                if existing_budget and existing_budget['id'] != '':
                    Budget.update(existing_budget['id'], amount)
                else:
                    b = Budget(m, year, amount)
                    Budget.create(b)

            return redirect('/budgets'), 303

        # if there are errors, return to the form with the errors
        months = DateHelper.months_in_year()
        current_month, current_year = DateHelper.current_month_year()
        budget = {
            "month": month,
            "year": year,
            "amount": amount
        }
        return render_template('budgets/_new_budget.html', months=months, curr_year=current_year, curr_month=current_month, budget=budget, errors=errors, repeat=repeat)
    except Exception as e:
        return str(e), 500


@app.route('/budgets', methods=['DELETE'])
def delete_budgets():
    ids = request.form.getlist('selected-budget')
    try:
        for id in ids:
            Budget.delete(id)
        budgets = Budget.find_all()
        return render_template('budgets/_partial.html', budgets=budgets)
    except Exception as e:
        return str(e), 500


@app.route('/budgets/current/edit', methods=['GET'])
def edit_current_budget():
    amount = request.args.get('amount', 0)
    id = request.args.get('id', '')

    return render_template('budgets/_edit_current_budget.html', amount=amount, id=id)


@app.route('/budgets/current/edit', methods=['PATCH'])
def update_current_budget():
    try:
        _action = request.form['_action']

        # cancel button, so just return
        if _action == 'cancel':
            return redirect('/'), 303

        budget_amount = float(request.form['budget'])
        error = Budget.validate_new_budget(budget_amount)
        if error:
            return error, 400

        #update budget
        id = request.form['budget_id']
        new_budget = Budget.update(id, budget_amount)

        first_day, last_day = DateHelper.month_range()

        # total expenses for this month
        total_expenses = Expense.find_by_month(first_day, last_day)
        balance = budget_amount - total_expenses

        stats = {
            "total_expenses": f"{total_expenses:.2f}",
            "budget": f"{budget_amount :.2f}",
            "balance": f"{balance:.2f}"
        }

        return render_template('overview/_stats.html', stats=stats, budget=new_budget)
    except ValueError:
        return 'Invalid budget', 400

@app.route('/budgets/edit', methods=['GET'])
def edit_budget():
    amount = request.args.get('amount', 0)
    id = request.args.get('id', '')

    return render_template('budgets/_edit_budget.html', amount=amount, id=id)

@app.route('/budgets/edit', methods=['PATCH'])
def update_budget():
    try:
        _action = request.form['_action']
        id = request.form['budget_id']

        # cancel button, so just return
        if _action == 'cancel':
            existing_budget = Budget.find_by_id(id)
            return render_template('budgets/_budget_item.html', budget=existing_budget)

        budget_amount = float(request.form['budget'])
        error = Budget.validate_new_budget(budget_amount)
        if error:
            return error, 400

        #update budget
        id = request.form['budget_id']
        new_budget = Budget.update(id, budget_amount)

        return render_template('budgets/_budget_item.html', budget=new_budget)

    except ValueError:
        return 'Invalid budget', 400

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
