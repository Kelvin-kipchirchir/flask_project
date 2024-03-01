from flask import* 
import sqlite3

from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy
#import mysql.connector as mysql
app = Flask(__name__) #creating the Flask class object 
app.secret_key = "abc" 
Bootstrap(app)
conn=sqlite3.connect("empire.db")
print("Database opened successfully")
#conn.execute("create table Users(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER UNIQUE NOT NULL,username TEXT NOT NULL,email TEXT UNIQUE NOT NULL,phone TEXT NOT NULL)")
print("table created successfully")
conn.close()
 
#conn=mysql.connect(host="localhost",user="root",password="",database="empire")
#cur=conn.cursor()
#app.config["UPLOAD_FOLDER"]=""gallery"
#app.config["MAX_CONTENT-PATH"]=300 

 
@app.route('/') #routing 
def index():
    return render_template("index.html")


@app.route('/about/<name>/<int:age>') 
def about(name,age):
    return "This is an online platform"+name+"and age is %d"%age

@app.route("/logins",methods=["POST","GET"])
def logins():
     error = None
     if request.method == "POST" :
         if request.form["password"]!="Admin1234":
             error = "invalid password"
             return render_template("login.html",error=error) 
         else:
             flash("you have successfully logged in")
             result=request.form
             uname=request.form["name"]
             passwd=request.form["password"]
             session["name"]=request.form["name"]
         return render_template("dashboard.html") 
     else:
         return render_template("index.html")
        

@app.route("/viewprofile")
def profile():
    #name=request.cookies.get("name")
    #resp=make_response(render_template("profile.html",name=name))
    #return resp
    if "name" in session:
        name=session["name"]
        return render_template("profile.html",name=name)
    else:
        return "<p>Please login first</p>"


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/user/<uname>")
def dashboard(uname):
    return render_template("dashboard.html",name=uname)

@app.route("/sign_up")
def sign_up():
    return render_template("registration.html")

@app.route("/new_user",methods=["POST"])
def new_user():
    return "<p>will create a new user soon</p>"

@app.route("/add_users")
def add_users():
    return render_template("adduser.html")
@app.route("/savedetails",methods = ["POST","GET"])
def savedetails():
    msg = "msg"
    if request.method == "POST":
        try:
            username = request.form["username"]
            email = request.form["email"]
            phone = request.form["phone"]
            user_id = request.form["user_id"]
            with sqlite3.connect("empire.db") as conn:
                cur = conn.cursor()
                cur.execute("INSERT into Users(user_id,username,email,phone) VALUES (?,?,?,?)",(user_id,username,email,phone))
                conn.commit()
                msg = "User Created successfully"
        except:
            conn.rollback()
            msg = "you cannot add the employee to list"
        finally:
            return render_template("dashboard.html",msg = msg)
            conn.close()


@app.route("/all_users") 
def all_users():
    conn = sqlite3.connect("empire.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from Users")
    rows = cur.fetchall()
    return render_template("dashboard.html",rows = rows)   
#doing some response handling
#printing an error
@app.route("/error")
def error():
    #return "<h1>Bad request</h1>",400
    return "<p><strong>Enter correct password</strong></p>"

#redirecting to outside
@app.route("/redirects")
def redirects():
    return redirect("http://www.siko.com")

@app.route("/student/<id>")
def get_student(id):
    student=load_student(id)
    if not student:
        abort(404)
    return "<h1>Hello,%s</h1>"%student.name

@app.route("/cookie_response")
def cookie_response():
    response=make_response("<h1>This document comes with a cookie</h1>")
    response.set_cookie("answer","42")
    return response
#error handling in flask
@app.errorhandler(404)
def page_not_found(e):
     return render_template("404.html"),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500

@app.route("/fileupload",methods=["POST"])
def fileupload():
    if request.method == "POST":
        f=request.files["file"]
        f.save(f.filename)
        return render_template("profile.html",icon=f.filename)
    else:
        return "<p>Oppss!!! choose the right format</p>"
    


@app.route("/logout")
def logout():
    if "name" in session:
        session.pop("name",None)
        return render_template("index.html")
    else:
        return "<p>user already logged out</p>"

    
if __name__ =='__main__':  
    app.run(debug = True)  