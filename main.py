from flask import Flask, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import jwt
import os
from datetime import date

# Variable used to located the directory of the file
basedir = os.path.abspath(os.path.dirname(__file__))

# Defines the database
db = SQLAlchemy()

# Defines flask app
app = Flask(__name__)


# App configurations to set the location of the database, and disable the tracking of modificatons
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializes the database and connects it to the app
db.init_app(app)



# Table created named Employee
class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True, nullable = False)
    age = db.Column(db.Integer)
    dateJoined = db.Column(db.String(10), nullable = False)

    
    def __repr__(self):
        return f'<Name: {self.name}, Age: {self.age}, Date Joined: {self.dateJoined}>'



@app.route('/', methods=("GET", "POST"))
def index():
    return render_template('index.html')


# App route for the page to view the database
@app.route('/view', methods=("GET", "POST"))
def view():
    employed = Employee.query.all()
    return render_template('view.html', employees=employed, public = True)

@app.route('/<int:id>')
def viewSpecific(id):
    employee = Employee.query.get_or_404(id)
    return render_template('view_specific.html', employee=employee)

@app.route('/create', methods=("GET", "POST"))
def create():
    if request.method == 'POST':
        
        name = request.form['fullname']
        age = int(request.form['age'])
        dateJoined = date.today()
        createdEmployee = Employee(name=name, age=age, dateJoined=dateJoined)
        db.session.add(createdEmployee)
        db.session.commit()

        return redirect(url_for('view'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=("GET", "POST"))
def edit(id):
    employee = Employee.query.get_or_404(id)
    
    if request.method == "POST":
        name = request.form['fullname']
        age = int(request.form['age'])
        dateJoined = date.today()
        
        employee.name = name
        employee.age = age
        employee.dateJoined = dateJoined
        
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('view'))
    return render_template('edit.html', employee=employee)


@app.route('/<int:id>/delete', methods=("GET", "POST"))
def delete(id):
    employee = Employee.query.get_or_404(id)
    
    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('view'))
    except:
        return "Unsuccessfull"

@app.route('/reset')
def reset():
    return render_template('reset.html')


@app.route('/reset/confirmed', methods=("GET", "POST"))
def reset_confirmed():
    db.drop_all()
    db.create_all()
    employed = Employee.query.all()
    return render_template('view.html', employees=employed)

# Runs the program
if __name__ == "__main__":
    app.app_context().push()
    app.run(debug=True)