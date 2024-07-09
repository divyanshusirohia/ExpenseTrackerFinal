from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import datetime

app = Flask(__name__)

load_dotenv()
app.config['DEBUG']=os.environ.get('FLASK_DEBUG')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Expense('{self.expense}', {self.amount})"

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_expenditure = sum([expense.amount for expense in expenses])
    return render_template('index.html', expenses=expenses, total_expenditure=total_expenditure)

@app.route('/add', methods=['POST'])
def add_expense():
    expense = request.form['expense']
    amount = float(request.form['amount'])
    new_expense = Expense(expense=expense, amount=amount)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/api/expenses')
def get_expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return jsonify([
        {
            'id': expense.id,
            'expense': expense.expense,
            'amount': expense.amount,
            'date': expense.date.strftime('%Y-%m-%d %H:%M:%S')
        } for expense in expenses
    ])

if __name__ == '__main__':
    app.run()