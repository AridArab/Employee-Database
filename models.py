from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os


# Variable used to located the directory of the file
basedir = os.path.abspath(os.path.dirname(__file__))

# Defines the database
db = SQLAlchemy()

# Table created named Employee
class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True, nullable = False)
    age = db.Column(db.Integer, unique = False, nullable = False)
    birthday = db.Column(db.String(13), unique = False, nullable = False)
    worktype = db.Column(db.String(20), unique = False, nullable = False)
    job = db.Column(db.String(30), unique = False, nullable = False)
    pay = db.Column(db.Integer, unique = False, nullable = False)
    bio = db.Column(db.String(150), unique = False, nullable = False)
    dateJoined = db.Column(db.String(10), nullable = False)

    
    def __repr__(self):
        return (f"Name: {self.name} ID: {self.id}")