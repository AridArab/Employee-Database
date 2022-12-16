from flask import Flask, request, render_template, url_for, flash, redirect
from datetime import date
from models import db, basedir, Employee
import uuid
import os


# Defines flask app
app = Flask(__name__)


# App configurations to set the location of the database, and disable the tracking of modificatons
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = '958e1be3-0c1b-4399-8938-7b346f7337dd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializes the database and connects it to the app
db.init_app(app)

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

@app.route('/<int:id>', methods=("GET", "POST"))
def viewSpecific(id):

    employee = Employee.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('view'))

    return render_template('view_specific.html', employee=employee)

@app.route('/create', methods=("GET", "POST"))
def create():

    if request.method == 'POST':

        name = request.form['fullname']
        age = request.form['age']
        birthday = request.form['birthdate']
        worktype = request.form['typeofwork']
        job = request.form['job']
        pay = request.form['money']
        bio = request.form['bio']

        if not name or not age:

            flash("Please enter valid values")

        else:

            dateJoined = date.today()

            createdEmployee = Employee(name=name, age=age, birthday=birthday, worktype=worktype, job=job, pay=pay, bio=bio, dateJoined=dateJoined)

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
        birthday = request.form['birthdate']
        worktype = request.form['typeofwork']
        job = request.form['job']
        pay = request.form['money']
        bio = request.form['bio']

        if not name or not age:

            flash("Please enter the new values")

        else:

            dateJoined = date.today()
            employee.name = name
            employee.age = int(age)
            employee.birthday = birthday
            employee.worktype = worktype
            employee.job = job
            employee.pay = pay
            employee.bio = bio
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
    entered = request.args.get('searched').lower()

    if isinstance(entered, str):

        for i in listdb:

            if entered in str(i).lower():

                resulted.append(str(i)[2:-3])

        return render_template('search.html', resulted=resulted, Employee=Employee, entered=entered)

    return render_template('search.html', listdb=listdb, Employee=Employee, entered=entered)




# Runs the program
if __name__ == "__main__":
    app.app_context().push()
    app.run(debug=True)