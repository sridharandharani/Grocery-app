import os.path

from flask import Flask, render_template, request
import sqlite3 as sql

from werkzeug.utils import redirect, secure_filename


connection = sql.connect("Wrapup.db", check_same_thread=False)

listofusers = connection.execute("select name from sqlite_master where type='table' AND name='user'").fetchall()
listofproducts = connection.execute("select name from sqlite_master where type='table' AND name='admin'").fetchall()

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

if listofproducts != []:
    print("Table exist already")
else:
    connection.execute('''create table admin(
                             ID integer primary key autoincrement,
                             category text,
                             product_name text,
                             price integer,
                             image blob

                             );''')
    print("Table Created Successfully")


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static\image"

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("base.html")

@app.route("/userdashboard", methods=["POST", "GET"])
def mainpage():
    return render_template("userdashboard.html")

@app.route("/register", methods=["POST", "GET"])
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
            return redirect("/userlogin")
        except Exception as e:
            print("Error occured ", e)

    return render_template("register.html")

@app.route("/userlogin", methods=["POST", "GET"])
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

@app.route("/adminlogin", methods=["POST", "GET"])
def adminlogin():
    if request.method == "POST":
        getusername = request.form["username"]
        getpassword = request.form["pass"]
        print(getusername)
        print(getpassword)
        if getusername == "wrappers" and getpassword == "82200":
            return redirect("/addproducts")
    return render_template("adminlogin.html")


@app.route("/addproducts", methods=["POST", "GET"])
def addproducts():
    if request.method == "POST":
            upload_image = request.files["image"]
            if upload_image!='':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'],upload_image.filename)
                upload_image.save(filepath)
                getcategory = request.form["category"]
                getproductname = request.form["productname"]
                getprice = request.form["price"]
                print(getcategory)
                print(getproductname)
                print(getprice)
                try:
                    cursor = connection.cursor()
                    cursor.execute("insert into admin(category,product_name,price,image)\
                                                   values('" + getcategory + "','" + getproductname + "'," + getprice + ",'" + upload_image.filename + "')")
                    connection.commit()
                    print(" Data Added Successfully.")
                    return redirect("/adminview")
                except Exception as e:
                    print("Error occured ", e)

    return render_template("addproducts.html")


@app.route("/adminview")
def admin_viewProducts():
    cursor = connection.cursor()
    cursor.execute("select * from admin")
    result = cursor.fetchall()
    return render_template("admin_view.html", products=result)
if __name__ == "__main__":
    app.run(debug=True)