import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy 

from sqlalchemy.sql import func


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

class student_data(db.Model):
    Serial = db.Column(db.Integer,primary_key = True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Phone = db.Column(db.Integer())

db.create_all()




@app.route('/')
def home():
   student_list = student_data.query.all()
   return render_template("index2.html", students=student_list)



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        my_data = student_data(Name=name,Email=email,Phone=phone)
        db.session.add(my_data)
        db.session.commit()
        return redirect(url_for('home'))




@app.route('/delete/<int:serial_id>', methods = ['GET'])
def delete(serial_id):
    del_student = db.session.query(student_data).filter(student_data.Serial == serial_id).first()
    db.session.delete(del_student)
    db.session.commit()

    return redirect(url_for('home'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        serial_id = request.form['id']
        
        update_student = db.session.query(student_data).filter(student_data.Serial == serial_id).first()
        update_student.Name = request.form['name']
        update_student.Email = request.form['email']
        update_student.Phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('home'))




if __name__ == "__main__":
    app.run(debug=True)
