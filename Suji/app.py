import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

# Route to the main page
@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])

def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) #Then save the file
        return "File has been uploaded."
    return render_template('index.html',form=form)

def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
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
            category TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Create the database and table on app startup
create_database()


app = Flask(__name__)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    date = request.form['date'] 
    description = request.form['description']
    amount = float(request.form['amount'])
    category = request.form['category']

    # Insert the transaction data into the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (date, description, amount, category)
        VALUES (?, ?, ?, ?)
    ''', (date, description, amount, category))

    conn.commit()
    conn.close()

    # Redirect to the home page or any other page after adding the transaction
    return redirect(url_for('index'))


@app.route('/')
def index():
    # Retrieve transactions from the database
    conn = sqlite3.connect('finance_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, date, description, amount, category FROM transactions')
    transactions = cursor.fetchall()
    conn.close()

    # Render the index.html template with the transactions data
    return render_template('index.html', transactions=transactions)
