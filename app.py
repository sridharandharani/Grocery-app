from flask import Flask, request, session, render_template
import sqlite3 as sql

from werkzeug.utils import redirect

connection = sql.connect("Adminmodule.db", check_same_thread=False)
listofproducts = connection.execute("select name from sqlite_master where type='table' AND name='admin'").fetchall()

if listofproducts != []:
    print("Table exist already")
else:
    connection.execute('''create table admin(
                             ID integer primary key autoincrement,
                             email text,
                             password varchar,
                             category text,
                             product_name text,
                             price integer

                             );''')
    print("Table Created Successfully")

admin = Flask(__name__)


@admin.route("/", methods=["POST", "GET"])
def adminlogin():
    if request.method == "POST":
        getusername = request.form["username"]
        getpassword = request.form["pass"]
        print(getusername)
        print(getpassword)
        if getusername == "wrappers" and getpassword == "82200":
            return redirect("/addproducts")
    return render_template("adminlogin.html")


@admin.route("/addproducts", methods=["POST", "GET"])
def addproducts():
    if request.method == "POST":
        getcategory = request.form["category"]
        getproductname = request.form["productname"]
        getprice = request.form["price"]
        print(getcategory)
        print(getproductname)
        print(getprice)
        try:
            connection.execute("insert into admin(category,product_name,price)\
                               values('" + getcategory + "','" + getproductname + "'," + getprice + ")")
            connection.commit()
            print(" Data Added Successfully.")
            return redirect("/adminview")
        except Exception as e:
            print("Error occured ", e)

    return render_template("addproducts.html")


@admin.route("/adminview")
def admin_viewProducts():
    cursor = connection.cursor()
    cursor.execute("select * from admin")
    result = cursor.fetchall()
    return render_template("admin_view.html", products=result)


if __name__ == "__main__":
    admin.run(debug=True)