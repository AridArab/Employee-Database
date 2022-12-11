from flask import Flask, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
#from wtforms import 
import jwt
import os



# Variable used to located the directory of the file
basedir = os.path.abspath(os.path.dirname(__file__))

# Defines the database
db = SQLAlchemy()

# Defines flask app
app = Flask(__name__)


# App configurations to set the location of the database, and disable the tracking of modificatons
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = '6d22d47e-cca3-4e44-8f89-0883a7b38f61'
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
        return (f"Name: {self.name} ID: {self.id}")



@app.route('/', methods=("GET", "POST"))
def index():
    if request.method == "POST":
        return redirect('view')
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
        age = (request.form['age'])
        if not name or not age:
            flash("Please enter valid values")
        else:
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
        age = request.form['age']
        if not name or not age:
            flash("Please enter the new values")
        else:
            dateJoined = date.today()
            employee.name = name
            employee.age = int(age)
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

@app.route('/reset', methods=("GET", "POST"))
def reset():
    if request.method == "POST":
        db.drop_all()
        db.create_all()
        return redirect(url_for('view'))
    return render_template('reset.html')

@app.route('/search', methods=('GET', 'POST'))
def search():
    resulted = []
    listdb = Employee.query.with_entities(Employee.name).all()
    entered = request.args.get('searched')
    if isinstance(entered, str):
        for i in listdb:
            if entered in str(i):
                resulted.append(str(i)[2:-3])
        return render_template('search.html', resulted=resulted, Employee=Employee)
    return render_template('search.html', listdb=listdb, Employee=Employee)




# Runs the program
if __name__ == "__main__":
    app.app_context().push()
    app.run(debug=True)