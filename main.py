from flask import Flask, render_template, render_template_string, request, redirect, jsonify, abort, Response
from flask_cors import CORS
from models.category import Category, CategoryExistsError, CategoryNotFoundError
from models.expenses import Expense
from models.budget import Budget
from models.datehelper import DateHelper
import sqlite3
import datetime


app = Flask(__name__)
# enable CORS for all API routes
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# -------------------------
# INDEX (OVERVIEW)
# -------------------------
@app.route('/', methods=['GET'])
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

        ctx = {
            "stats": {
                "total_expenses": f"{total_expenses:.2f}",
                "budget": f"{budget['amount']:.2f}",
                "balance": f"{balance:.2f}"
            },
            "expenses": latest_expenses,
            "budget": budget,
            "today": today,
            "disable_delete": True  # disable delete button for expenses
        }

        return render_template('index.html', ctx=ctx)
    except Exception as e:
        abort(500, description="Could not load overview page")


# -------------------------
# EXPENSES
# -------------------------
@app.route('/expenses', methods=['GET'])
def expenses_route():
    try:
        q = request.args.get('q', '')
        cat = request.args.get('category', 'all')
        page = int(request.args.get('page', 0))
        expenses, cnt, has_next_page = Expense.find_many(page, q, cat)
        categories = Category.find_all()

        ctx = {
            "expenses": expenses,
            "cnt": cnt,
            "has_next_page": has_next_page,
            "categories": categories,
        }

        is_load_more = request.headers.get('Hx-Trigger') == 'load-more'

        # on load more, return a partial
        template = 'expenses/_partial.html' if is_load_more else 'expenses.html'

        return render_template(template, ctx=ctx, page=page)
    except Exception as e:
        # inline error for load more
        if is_load_more:
            # return a span because we need to use HX-Reselect to select the whole error message to replace
            return Response("<span>Could not load expenses</span>", 500, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML', 'HX-Reselect': '*'})

        abort(500, description="Could not load expenses")


@app.route('/api/expenses', methods=['GET'])
def expenses_json():
    try:
        q = request.args.get('q', '')
        cat = request.args.get('category', 'all')
        page = int(request.args.get('page', 0))

        if page < 0:
            raise ValueError()

        expenses, cnt = Expense.find_many(page, q, cat)
        return jsonify({"count": cnt, "page": page, "expenses": expenses})

    except ValueError as ve:
        return jsonify({'error': 'Invalid page number'}), 400

    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500


@app.route('/expenses/new', methods=['GET'])
def new_expense_form():
    try:
        categories = Category.find_all()
        ctx = {
            "categories": categories,
            "expense": {},
            "errors": {}
        }

        return render_template('new_expense.html', ctx=ctx)
    except Exception as e:
        abort(500, description="Could not load page")


@app.route('/expenses/new', methods=['POST'])
def create_new_expense():
    title = request.form.get('title', '')
    amount = float(request.form.get('amount', 0))
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

            ctx = {
                "categories": categories,
                "expense": e,
                "errors": errors
            }

            return render_template('new_expense.html', ctx=ctx)
    except Exception as e:
        return Response("Server error while creating budget", 500, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})


@app.route('/expenses', methods=['DELETE'])
def delete_expenses():
    ids = request.form.getlist('selected-expense')
    q = request.args.get('q', '')
    cat = request.args.get('category', '')
    try:
        for id in ids:
            Expense.delete(id)
        expenses, cnt, has_next_page = Expense.find_many(0, q, cat)
        categories = Category.find_all()

        ctx = {
            "expenses": expenses,
            "cnt": cnt,
            "has_next_page": has_next_page,
            "categories": categories,
        }

        return render_template('expenses/_partial.html', ctx=ctx, page=0)
    except Exception as e:
        return Response("Server error while deleting expense", 500, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})

# -------------------------
# BUDGETS
# -------------------------


@app.route('/budgets', methods=['GET'])
def budgets_route():
    try:
        budgets = Budget.find_all()

        return render_template('budgets.html', budgets=budgets)
    except Exception as e:
        abort(500, description="Could not load budgets")


@app.route('/budgets/new', methods=['GET'])
def new_budget_form():
    try:
        months = DateHelper.months_in_year()
        current_month, current_year = DateHelper.current_month_year()

        ctx = {
            "months": months,
            "curr_year": current_year,
            "curr_month": current_month,
            "budget": {},
            "errors": {}
        }

        return render_template('new_budget.html', ctx=ctx)
    except Exception as e:
        abort(500, description="Could not load page")


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

        ctx = {
            "months": months,
            "curr_year": current_year,
            "curr_month": current_month,
            "budget": {
                "month": month,
                "year": year,
                "amount": amount
            },
            "errors": errors,
            "repeat": repeat
        }

        return render_template('new_budget.html', ctx=ctx)
    except Exception as e:
        return Response("Server error while creating budget", 500, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})


@app.route('/budgets', methods=['DELETE'])
def delete_budgets():
    ids = request.form.getlist('selected-budget')
    try:
        for id in ids:
            Budget.delete(id)
        budgets = Budget.find_all()
        return render_template('budgets/_partial.html', budgets=budgets)
    except Exception as e:
        return Response("Server error while deleting budget", 500, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})


@app.route('/budgets/current/edit', methods=['GET'])
def edit_current_budget():
    try:
        amount = request.args.get('amount', 0)
        id = request.args.get('id', '')
    except Exception as e:
        return Response("Could not load current budget", 500, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})

    return render_template('budgets/_edit_current_budget.html', amount=amount, id=id)


@app.route('/budgets/current/edit', methods=['PATCH'])
def update_current_budget():
    try:
        _action = request.form['_action']
        budget_amount = float(request.form['budget'])
        id = request.form['budget_id']

        # save button, so validate and save
        if _action == 'save':
            error = Budget.validate_new_budget(budget_amount)
            if error:
                return error, 400

            # update budget
            new_budget = Budget.update(id, budget_amount)

        # cancel button, get the existing budget
        if _action == 'cancel':
            existing_budget = Budget.find_by_id(id)

        # get data for stats
        first_day, last_day = DateHelper.month_range()

        # total expenses for this month
        total_expenses = Expense.find_by_month(first_day, last_day)
        balance = budget_amount - total_expenses

        ctx = {
            "stats": {
                "total_expenses": f"{total_expenses:.2f}",
                "budget": f"{budget_amount :.2f}",
                "balance": f"{balance:.2f}"
            },
            "budget": new_budget if _action == 'save' else existing_budget
        }

        return render_template('overview/_stats.html', ctx=ctx)
    except ValueError:
        return Response("Invalid budget", 400, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})
    except Exception as e:
        return Response("Could not update budget", 500, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})


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
            raise ValueError()

        # update budget
        id = request.form['budget_id']
        new_budget = Budget.update(id, budget_amount)

        return render_template('budgets/_budget_item.html', budget=new_budget)

    except ValueError:
        return Response("Invalid budget", 400, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})

    except Exception as e:
        return Response("Could not update budget", 500, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})

# -------------------------
# CATEGORIES
# -------------------------


@app.route('/categories', methods=['GET'])
def categories_route():
    try:
        categories = Category.find_all()
        return render_template('categories.html', categories=categories)
    except Exception as e:
        abort(500, description="Could not load categories")


@app.route('/categories', methods=['POST'])
def new_category():
    try:
        c = Category.create(request.form['name'])
    except (CategoryExistsError, ValueError) as e:
        return Response(str(e), 400, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})

    except Exception as e:
        return Response("Error while creating category", 500, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})

    return render_template('categories/_category_item.html', category=c)


@app.route('/categories/<id>', methods=['DELETE'])
def delete_category(id):
    try:
        Category.delete(id)
        return '', 200
    except sqlite3.IntegrityError as e:
        return Response('Cannot delete a category that has expenses', 400, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})
    except CategoryNotFoundError as e:
        return Response(str(e), 400, {'HX-Retarget': '#error', 'HX-Reswap': 'innerHTML'})

# -------------------------
# INSIGHTS
# -------------------------


@app.route('/insights', methods=['GET'])
def insights_route():
    curr_year = datetime.datetime.now().year

    try:
        year = int(request.args.get('year', curr_year))

        if year != curr_year and year != curr_year - 1:
            raise ValueError()
    except ValueError as e:
        abort(400, description="Invalid year")

    try:
        months = DateHelper.months_in_year()

        totals, cnt, highest = Expense.total_per_month(year)
        # Create a dictionary to map months to expenses
        expense_dict = {month: expense for expense, month in totals}

        # Generate a new list with 0 for months without expenses
        expenses_list = [round(expense_dict.get(month, 0), 2)
                         for month in range(1, 13)]

        totals_per_category = Expense.expenses_per_category(year)

        insights_data = {
            "expenses": {
                "count": cnt,
                "yearly_total": sum(expenses_list),
                "total_per_month": expenses_list,
                "highest": highest,
                "highest_month": months[expenses_list.index(max(expenses_list))]['name'] if max(expenses_list) > 0 else None,
            },
            "categories": {
                "labels": [str(c[1]) for c in totals_per_category],
                "amounts": [c[0] for c in totals_per_category]
            }
        }

        return render_template('insights.html', data=insights_data, curr_year=curr_year, selected_year=year)
    except Exception as e:
        abort(500, description="Could not load insights")

# -------------------------
# error handlers
# -------------------------


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/page_not_found.html'), 404


@app.errorhandler(400)
def bad_request(error):
    return render_template('error/error.html', title="Bad Request", error=error.description), 400


@app.errorhandler(405)
def not_allowed(error):
    return render_template('error/error.html', title="Method Not Allowed", error=error.description), 405


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/error.html', title="Internal Server Error", error=error.description), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
