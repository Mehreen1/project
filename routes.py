import os, json
from werkzeug.utils import validate_arguments
from wtforms.validators import InputRequired, Email, Length, NoneOf
from flask import Flask, render_template, request, redirect, url_for, session , flash
from flask_wtf import FlaskForm 
from wtforms import SubmitField, StringField 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__,template_folder='template')

app.secret_key= "fPtn"
engine = create_engine("mysql+pymysql://root:mkroot@localhost:3306/miniproject")

db = scoped_session(sessionmaker(bind=engine)) 

class Sform(FlaskForm):  
    submit = SubmitField('Submit') 
# .............................. sign in...........................
@app.route('/')
def sign():
    return render_template('signin.html')

@app.route('/sign_in', methods = ['GET', 'POST'])
def sig(): 
      if request.method == "POST":  
        F_Name =  request.form.get("F_Name")
        L_Name  = request.form.get("L_Name") 
        email =  request.form.get("email")
        password = request.form.get("password")
        db.execute("INSERT into sign(F_Name, L_Name, email, password) VALUES (:F_Name, :L_Name, :email, :password)",
                   {"F_Name":F_Name ,"L_Name":L_Name,"email": email, "password": password})
        db.commit()
        if email.lower():
           session['email'] = [0][0]
        sign = db.execute("SELECT * FROM sign").fetchall()
        return redirect("/home" )
      else:
        sign = db.execute("SELECT * FROM sign").fetchall()  
        return render_template("signin.html", sign=sign)


@app.route("/signout")
def signO():

    session.clear()
    return redirect(url_for('sig'))

@app.route("/update/<int:id>/", methods=['POST','GET'])
def update(id):
    if request.method=="POST":
        F_Name = request.form.get("F_Name")
        L_Name = request.form.get("L_Name")
        email = request.form.get("email")
        password = request.form.get("password")
        db.execute("Update sign SET F_Name = :F_Name ,L_Name=:L_Name, email = :email, password = :password, where id = :id",
                {"F_Name": F_Name, "L_Name":L_Name,"email": email, "password" :password ,"id":id})
        db.commit()
        return redirect(url_for('sign'))
    else:
        sign = db.execute("SELECT * FROM sign WHERE id = :id", {"id": id}).fetchone()
        return render_template("update.html", sign=sign, id=id)

@app.route("/update_now/<int:id>/", methods=['POST', 'GET'])
def update_now(id):
    sign = db.execute("SELECT * FROM sign WHERE id = :id", {"id": id}).fetchone()
    if sign is None:
        return "No record found by ID = " + str(id) +". Kindly go back to <a href='/sign'> sig </a>"
    else:
        sign = db.execute("delete FROM login WHERE id = " + str(id))
        db.commit()
        return redirect(url_for('sign'))

@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    sign = signO.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if signO:
            db.session.delete(sign)
            db.session.commit()
            return redirect('/data')
    return render_template('delete.html')

# ..................................log in ......................

@app.route("/login", methods=['GET'])
def index():

        return render_template("login.html" )

@app.route("/login", methods=['POST','GET'])
def log():
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db.execute("INSERT into login( email, password) VALUES (:email, :password)",
                   {"email": email, "password": password})
        db.commit()
        if email.lower():
            session['email'] = [0][0]

            return redirect("/home")
        else:
         flash( "Incorrect Usrname and Password")
         return render_template("login.html",flash=flash)

# ............................Logout ....................
@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for('index'))



#........................ home pages  ...................


@app.route('/home')
def home():
    form = Sform()
    # if Sform.validate_on_submit:
    #     flash("successfully")
    #     return render_template("home.html",form=form)
    # else:
    return render_template("home.html",form=form)

@app.route('/homepage', methods = ['GET', 'POST'])
def homepage():
      form = Sform()
      if request.method == "POST":   
        F_Name =  request.form.get("F_Name")
        L_Name  = request.form.get("L_Name")
        email = request.form.get("email")
        Contect_Number = request.form.get("Contect_Number")  
        message = request.form.get("message")

        db.execute("INSERT into home(F_Name, L_Name, Contect_Number, email,message) VALUES (:F_Name, :L_Name, :Contect_Number, :email,  :message)",
                   {"F_Name":F_Name ,"L_Name":L_Name, "Contect_Number" :Contect_Number, "email":email ,"message":message})
        db.commit()
        if Sform.validate_on_submit:
            flash("successfully")
        # return render_template("home.html",form=form)
        home = db.execute("SELECT * FROM home").fetchall()
        return redirect(url_for("home",home=home,form=form))
      else:
        flash("Not successfully")
        return render_template("home.html",form=form)

  

# ..............................About.............
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
   app.run(debug = True)