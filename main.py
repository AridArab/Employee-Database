from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()

class Employee(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)
    

    def __repr__(self):
        return f'<Employee: {self.name} Age: {self.age}>'


class Administrator(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), unique=True, nullable=True)
    password = db.Column(db.String(100), unique=True, nullable=True)


    def __repr__(self):
        return f'<Admin: {self.user}>'


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)