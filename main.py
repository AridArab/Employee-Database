from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os

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
    
    def __repr__(self):
        return f'<Name: {self.name}, Age: {self.age}>'


# App route for the index
@app.route('/')
def index():
    employed = Employee.query.all()
    return render_template('index.html', employees=employed, public = True)


# Runs the program
if __name__ == "__main__":
    app.app_context().push()
    app.run(debug=True)