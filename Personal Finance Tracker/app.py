import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask import jsonify
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from sqlalchemy import func
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

# Function to create the database and table if they don't exist
def create_database():
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            type TEXT NOT NULL CHECK(type IN ('Income', 'Expense')) -- Add this line
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS net_worth (
            id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            networth REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Create the database and table on app startup
create_database()

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) #Then save the file
        return "File has been uploaded."
    return render_template('index.html',form=form)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    date = request.form['date'] 
    description = request.form['description']
    amount = float(request.form['amount'])
    category = request.form['category']
    type = request.form['type'] 

    # Insert the transaction data into the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (date, description, amount, category, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, description, amount, category, type))

    conn.commit()
    conn.close()

    # Redirect to the transactions page after adding the transaction
    return redirect(url_for('transactions'))

@app.route('/add_net_worth', methods=['POST'])
def add_net_worth():
    date = request.form['networth_date'] 
    net_worth = float(request.form['networth_value']) 

    # Insert the net worth data into the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO net_worth (date, networth)
        VALUES (?, ?)
    ''', (date, net_worth))

    conn.commit()
    conn.close()

    # Redirect to the net worth page after adding the net worth
    return redirect(url_for('net_worth'))

@app.route('/net_worth')
def net_worth():
    # Retrieve net worth data from the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, date, networth FROM net_worth')
    net_worths = cursor.fetchall()
    conn.close()

    # Convert the net worths list of tuples into list of dictionaries
    net_worths_dict = []
    for net_worth in net_worths:
        net_worth_dict = {
            "id": net_worth[0],
            "date": net_worth[1],
            "networth": net_worth[2]
        }
        net_worths_dict.append(net_worth_dict)

    # Render the networth.html template with the net worth data
    return render_template('networth.html', networths=net_worths_dict)

@app.route('/delete_net_worth/<int:id>', methods=['POST'])
def delete_net_worth(id):
    # Delete the net worth data from the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM net_worth WHERE id = ?
    ''', (id,))

    conn.commit()
    conn.close()

    # Redirect to the net worth page after deleting the net worth
    return redirect(url_for('net_worth'))

@app.route('/delete_transaction/<int:id>', methods=['POST'])
def delete_transaction(id):
    # Delete the transaction data from the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM transactions WHERE id = ?
    ''', (id,))

    conn.commit()
    conn.close()

    # Redirect to the transactions page after deleting the transaction
    return redirect(url_for('transactions'))

@app.route('/transactions')
def transactions():
    # Retrieve filter parameters from the request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')

    # Create the query dynamically based on provided filters
    query = 'SELECT id, date, description, amount, category, type FROM transactions WHERE 1=1' 
    params = []

    if start_date:
        query += ' AND date >= ?'
        params.append(start_date)

    if end_date:
        query += ' AND date <= ?'
        params.append(end_date)

    if category:
        query += ' AND category = ?'
        params.append(category)

    # Retrieve transactions from the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    transactions = cursor.fetchall()
    conn.close()

    # Convert the transactions list of tuples into list of dictionaries
    transactions_dict = []
    for transaction in transactions:
        transaction_dict = {
            "id": transaction[0],
            "date": transaction[1],
            "description": transaction[2],
            "amount": transaction[3],
            "category": transaction[4],
            "type": transaction[5]  # Add this line
        }
        transactions_dict.append(transaction_dict)

    # Render the transactions.html template with the transactions data
    return render_template('transactions.html', transactions=transactions_dict)

# Function to insert transactions into the database
def insert_transactions(transactions):
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()

    for transaction in transactions:
        date, amount, category, description, type = transaction
        cursor.execute('''
            INSERT INTO transactions (date, description, amount, category, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, description, amount, category, type))

    conn.commit()
    conn.close()

# Sample data for transactions (25 expenses and 10 incomes)
transactions_data = [
    # Expense transactions
    ("2023-07-01", 35.50, "Beauty", "Skin care products", "Expense"),
    ("2023-07-02", 12.75, "Food", "Lunch at a restaurant", "Expense"),
    ("2023-07-03", 25.00, "Supplies", "Office stationery", "Expense"),
    ("2023-07-04", 18.99, "Entertainment", "Movie ticket", "Expense"),
    ("2023-07-05", 40.00, "Fitness", "Gym membership", "Expense"),
    ("2023-07-06", 8.99, "Food", "Snacks", "Expense"),
    ("2023-07-07", 65.00, "Entertainment", "Concert tickets", "Expense"),
    ("2023-07-08", 30.25, "Supplies", "Home cleaning products", "Expense"),
    ("2023-07-09", 15.50, "Beauty", "Makeup", "Expense"),
    ("2023-07-10", 20.00, "Fitness", "Yoga class", "Expense"),
    ("2023-07-11", 50.00, "Food", "Groceries", "Expense"),
    ("2023-07-12", 100.00, "Entertainment", "Amusement park", "Expense"),
    ("2023-07-13", 22.99, "Supplies", "School supplies", "Expense"),
    ("2023-07-14", 60.00, "Fitness", "Personal trainer", "Expense"),
    ("2023-07-15", 10.00, "Beauty", "Nail polish", "Expense"),
    ("2023-07-16", 45.50, "Food", "Dinner at a restaurant", "Expense"),
    ("2023-07-17", 28.75, "Entertainment", "Movie rental", "Expense"),
    ("2023-07-18", 36.00, "Supplies", "Art materials", "Expense"),
    ("2023-07-19", 22.00, "Fitness", "Workout clothes", "Expense"),
    ("2023-07-20", 70.00, "Food", "Takeout", "Expense"),
    ("2023-07-21", 90.00, "Entertainment", "Video games", "Expense"),
    ("2023-07-22", 15.99, "Supplies", "Kitchen supplies", "Expense"),
    ("2023-07-23", 55.00, "Fitness", "Running shoes", "Expense"),
    ("2023-07-24", 25.50, "Beauty", "Hair products", "Expense"),
    ("2023-07-25", 40.00, "Food", "Dining out", "Expense"),

    # Income transactions
    ("2023-07-01", 2000.00, "Salary", "Monthly Salary", "Income"),
    ("2023-07-10", 500.00, "Bonus", "Performance bonus", "Income"),
    ("2023-07-15", 1200.00, "Freelance", "Design project payment", "Income"),
    ("2023-07-18", 800.00, "Side Hustle", "Tutoring income", "Income"),
    ("2023-07-25", 1500.00, "Salary", "Monthly Salary", "Income"),
    ("2023-07-27", 300.00, "Investments", "Dividend income", "Income"),
    ("2023-07-29", 700.00, "Freelance", "Writing project payment", "Income"),
    ("2023-07-31", 1800.00, "Salary", "Monthly Salary", "Income"),
]

# Call the function to insert transactions into the database
insert_transactions(transactions_data)

@app.route('/categories')
def categories():
    # Connect to the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()

    # Execute the query to get all categories
    cursor.execute('SELECT DISTINCT category FROM transactions')

    # Fetch all rows from the executed query
    categories = cursor.fetchall()

    conn.close()

    # Convert the categories list of tuples into list of strings
    categories_list = [category[0] for category in categories]

    # Return the list of categories as a JSON response
    return jsonify(categories_list)

@app.route('/reports/spending_breakdown')
def spending_breakdown():
    # Retrieve the selected categories from the query parameters
    selected_categories = request.args.getlist('categories')

    # Connect to the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()

    if selected_categories:
        # Use tuple or string formatting depending on number of categories
        format_str = '(' + ','.join('?' for _ in selected_categories) + ')'
        # Execute the query to get the sum of amounts for each selected category
        cursor.execute(f'''
            SELECT category, SUM(amount)
            FROM transactions
            WHERE category IN {format_str}
            GROUP BY category
        ''', tuple(selected_categories))
    else:
        # Execute the query to get the sum of amounts for each category
        cursor.execute('''
            SELECT category, SUM(amount)
            FROM transactions
            GROUP BY category
        ''')

    # Fetch all rows from the executed query
    categories = cursor.fetchall()

    conn.close()

    # Convert the categories list of tuples into list of dictionaries
    categories_dict = []
    for category in categories:
        category_dict = {
            "category": category[0],
            "total": category[1]
        }
        categories_dict.append(category_dict)

    return render_template('spending_breakdown.html', categories=categories_dict, selected_categories=selected_categories)

@app.route('/reports/net_worth_over_time')
def net_worth_over_time():
    # Connect to the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()

    # Execute the query to get all net worth entries
    cursor.execute('SELECT date, networth FROM net_worth ORDER BY date ASC')

    # Fetch all rows from the executed query
    net_worth_entries = cursor.fetchall()

    conn.close()

    # Convert the net worth entries list of tuples into list of dictionaries
    net_worth_entries_dict = []
    for entry in net_worth_entries:
        entry_dict = {
            "date": entry[0],
            "networth": entry[1]
        }
        net_worth_entries_dict.append(entry_dict)

    return render_template('net_worth_over_time.html', networths=net_worth_entries_dict)

@app.route('/reports/income_vs_expenses')
def income_vs_expenses():
    return render_template('income_vs_expenses.html')

@app.route('/reports/income_vs_expenses_data')
def income_vs_expenses_data():
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()

    # Retrieve the start_date and end_date from the request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Adjust the query to filter by date, if necessary
    query = '''
        SELECT date, type, SUM(amount) 
        FROM transactions
    '''
    params = []

    if start_date or end_date:
        query += ' WHERE '
        if start_date:
            query += 'date >= ?'
            params.append(start_date)
        if end_date:
            if start_date:
                query += ' AND '
            query += 'date <= ?'
            params.append(end_date)

    query += ' GROUP BY date, type'
    
    cursor.execute(query, params)

    data = cursor.fetchall()
    conn.close()

    # Organize the data for the chart
    chart_data = {
        "dates": [],
        "income": [],
        "expenses": []
    }

    for row in data:
        date, type, amount = row

        if date not in chart_data["dates"]:
            chart_data["dates"].append(date)
            chart_data["income"].append(0)
            chart_data["expenses"].append(0)

        if type == 'Income':
            chart_data["income"][-1] = amount
        elif type == 'Expense':
            chart_data["expenses"][-1] = amount

    # Convert the dictionary into a JSON response
    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(debug=True)
