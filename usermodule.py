from flask import Flask, render_template, request
import sqlite3 as sql

from werkzeug.utils import redirect

connection = sql.connect("Usermodule.db", check_same_thread=False)
listofusers = connection.execute("select name from sqlite_master where type='table' AND name='user'").fetchall()

if listofusers != []:
    print("Table exist already")
else:
    connection.execute('''create table user(
                             ID integer primary key autoincrement,
                             name text,
                             phone_number integer,
                             email integer,
                             password varchar
                             )''')
    print("Table Created Successfully")

user = Flask(__name__)

@user.route("/",methods=["POST","GET"])
def home():
    return render_template("base.html")

@user.route("/userdashboard",methods=["POST","GET"])
def mainpage():
    return render_template("userdashboard.html")

@user.route("/register",methods=["POST","GET"])
def new_user():
    if request.method == "POST":
        getname = request.form["name"]
        getphone_number = request.form["phone_number"]
        getemail = request.form["email"]
        getpassword = request.form["password"]
        print(getname)
        print(getphone_number)
        print(getemail)
        print(getpassword)
        try:
            connection.execute("insert into user(name,phone_number,email,password)\
                                   values('" + getname + "'," + getphone_number + ",'" + getemail + "', '" + getpassword + "')")
            connection.commit()
            print("User Data Added Successfully!")
        except Exception as e:
            print("Error occured ", e)

    return render_template("register.html")

@user.route("/userlogin",methods=["POST","GET"])
def user_login():
    if request.method == "POST":
        getemail = request.form["email"]
        getpassword = request.form["password"]
        print(getemail)
        print(getpassword)
        if getemail != "1" and getpassword != "0":
            return redirect("/userdashboard")
    return render_template("userlogin.html")


# @user.route("/products")
# def user_viewProducts():
#     cursor = connection.cursor()
#     count = cursor.execute("select * from Products")
#     result = cursor.fetchall()
#     return render_template("products.html")

# @user.route("/searchproducts",methods=["POST","GET"])
# def user_search_book():
#     if request.method == "POST":
#         getproductname=request.form["name"]
#         print(getproductname)
#         cursor = connection.cursor()
#         count = cursor.execute("select * from book where productname='"+getproductname+"'")
#         result = cursor.fetchall()
#         return render_template("searchproduct.html", searchProduct=result)
#
#     return render_template("searchproduct.html")

if __name__=="__main__":
    user.run(debug=True)