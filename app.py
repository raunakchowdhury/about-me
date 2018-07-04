from flask import Flask, render_template, request, session, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whomst gonn guess this?'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)

from models import *
db.create_all()

@app.route('/')
def start():
    return render_template('login.html')

@app.route('/account_creation', methods=['GET','POST']) # methods can be either GET or POST, when you create accounts you use POST
def create_account():
    #Extracts data from form
    user = request.form.get('user')
    email = request.form.get('email')
    password = request.form.get('password')

    account = User(user,email,password)
    session['user'] = account.user #keeps track of what user is logged in
    db.session.add(account) #stores into RAM
    db.session.commit() #commits all additions/deletions to the db

    return render_template('hello.html', user=user)

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('user')
    email = request.form.get('email')
    password = request.form.get('password')

    account = User.query.filter_by(user=user,email=email,password=password).first() #returns a Query, a list of elements, and takes the first element
    # account is a User
    #.all() returns in a list
    if account == None:
        flash('Invalid account credentials!')
        #get_flashed_messages()
        return render_template('login.html')
    session['user'] = account.user #keeps track of what user is logged in
    return render_template('hello.html', user=account.user)

@app.route('/account_query') #auto set to GET
def account_query():
    account = User.query.filter_by(user=session['user']).first() #uses the session
    return render_template('hello.html', account=account, user=account.user)


if __name__ == '__main__':
    app.run(debug=True)
