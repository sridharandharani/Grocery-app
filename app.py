import os.path

import razorpay
from flask import Flask, render_template, request, session
from flask_session import Session
import sqlite3 as sql

from werkzeug.utils import redirect, secure_filename


connection = sql.connect("Wrapup.db", check_same_thread=False)

listofusers = connection.execute("select name from sqlite_master where type='table' AND name='user'").fetchall()
listofproducts = connection.execute("select name from sqlite_master where type='table' AND name='admin'").fetchall()
listofwrap = connection.execute("select * from sqlite_master where type='table' AND name='wrap'").fetchall()
listofbuy = connection.execute("select * from sqlite_master where type='table' AND name='buy'").fetchall()


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

if listofwrap !=[]:
    print("wrap table already exits")
else:
    connection.execute('''create table wrap(
                                ID integer primary key autoincrement,
                                admin_product_id integer,
                                user_id text );''')

if listofbuy !=[]:
    print("order table already exits")
else:
    connection.execute('''create table buy(
                                    ID integer primary key autoincrement,
                                    admin_product_id integer,
                                    user_id text );''')


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['UPLOAD_FOLDER'] = "static\image"

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("base.html")

@app.route("/userdashboard", methods=["POST", "GET"])
def mainpage():
    cursor = connection.cursor()
    if request.method == 'POST':
        getproductname = request.form["pname"]
        cursor.execute("select * from admin where product_name= '" + getproductname + "'")
        result = cursor.fetchall()
        if result is None:
            print("product does not exists ")
        else:
            return render_template("userdashboard.html", search=result, status=True)
    else:
        return render_template("userdashboard.html", search=[], status=False)

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

@app.route('/update',methods=['GET','POST'])
def Update_user():
    try:
        if request.method == 'POST':
            getname = request.form["newname"]
            print(getname)
            cursor = connection.cursor()
            count = cursor.execute("select * from user where name='" + getname + "' ")
            result = cursor.fetchall()
            print(len(result))
            return render_template("editprofile.html", searchname = result)
        return render_template("editprofile.html")
    except Exception as error:
        print(error)


@app.route('/edit',methods=['GET','POST'])
def User_edit():
    if request.method == 'POST':
        getName = request.form["newname"]
        getEmail = request.form["newemail"]
        getPhone = request.form["newphone"]
        getPass = request.form["newpass"]
        try:
            query = "update user set phone_number=" + getPhone + ",email='" + getEmail + "',password='" + getPass + "' where name='" + getName + "'"
            print(query)
            connection.execute(query)
            connection.commit()
            print("Edited Successfully")
            return redirect('/userlogin')
        except Exception as error:
            print(error)

    return render_template("editprofile.html")

@app.route("/userlogin", methods=["POST", "GET"])
def user_login():
    global Uid
    if request.method == "POST":
        getemail = request.form["email"]
        getpassword = request.form["password"]
        print(getemail)
        print(getpassword)
        cursor = connection.cursor()
        query = "select * from user where email='" + getemail + "' and password='" + getpassword + "' "
        result = cursor.execute(query).fetchall()
        if len(result) > 0:
            for i in result:
                getuName = i[1]
                getuId = i[0]
                session["name"] = getuName
                session["id"] = getuId
                Uid = str(session["id"])
            print("password correct")
            return redirect('/userdashboard')
        else:
            return render_template("userlogin.html", status=True)
    else:
        return render_template("userlogin.html", status=False)

@app.route("/adminlogin", methods=["POST", "GET"])
def adminlogin():
    global id
    if request.method == "POST":
        getusername = request.form["username"]
        getpassword = request.form["pass"]
        print(getusername)
        print(getpassword)
        if getusername == "wrappers" and getpassword == "82200":
            return redirect("/admindashboard")
    return render_template("adminlogin.html")

@app.route('/admindashboard',methods=["POST", "GET"])
def admin_dashboard():
    cursor = connection.cursor()
    if request.method == 'POST':
        getproductname = request.form["pname"]
        cursor.execute("select * from admin where product_name= '" + getproductname + "'")
        result = cursor.fetchall()
        if result is None:
            print("product does not exists ")
        else:
            return render_template("admindashboard.html", search=result, status=True)
    else:
        return render_template("admindashboard.html", search=[], status=False)


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

# @app.route('/update',methods=['GET','POST'])
# def admin_update():
#     try:
#         if request.method == 'POST':
#             getproductname = request.form["newname"]
#             print(getproductname)
#             cursor = connection.cursor()
#             count = cursor.execute("select * from admin where product_name='" + getproductname + "' ")
#             result = cursor.fetchall()
#             print(len(result))
#             return render_template("updateproducts.html", searchname = result)
#         return render_template("updateproducts.html")
#     except Exception as error:
#         print(error)
#
#
# @app.route('/updation',methods=['GET','POST'])
# def admin_edit():
#     if request.method == 'POST':
#         upload_image = request.files["image"]
#         if upload_image != '':
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload_image.filename)
#             upload_image.save(filepath)
#         getcategory = request.form["newcategory"]
#         getName = request.form["newpname"]
#         getprice = request.form["newprice"]
#         try:
#             query = "update admin set category='" + getcategory + "',product_name='" + getName + "',price=" + getprice +  " ,image='" + upload_image.filename + "' where product_name='" + getName + "'"
#             print(query)
#             connection.execute(query)
#             connection.commit()
#             print("Edited Successfully")
#             return redirect('/adminview')
#         except Exception as error:
#             print(error)
#
#     return render_template("updateproducts.html")

@app.route('/delete', methods=['GET', 'POST'])
def deletion():
    if request.method == "POST":
        getproductname = request.form["pname"]
        connection.execute("delete from admin where product_name='" + getproductname + "'")
        connection.commit()
        print("Deleted Successfully")
        return redirect('/adminview')
    return render_template("deleteproducts.html")


@app.route("/adminview")
def admin_viewProducts():
    cursor = connection.cursor()
    cursor.execute("select * from admin")
    result = cursor.fetchall()
    return render_template("admin_view.html", products=result)

@app.route("/products")
def user_viewProducts():
    cursor = connection.cursor()
    cursor.execute("select * from admin")
    result = cursor.fetchall()
    return render_template("products.html", products=result)

@app.route("/vegetables")
def view_vegetables():
    lower_amt = str(1)
    higher_amt = str(50)
    cursor = connection.cursor()
    cursor.execute("Select * From admin Where price Between "+lower_amt+" And "+higher_amt)
    result = cursor.fetchall()
    return render_template("vegetables.html", products=result)

@app.route("/fruits")
def view_fruits():
    lower_amt = str(100)
    higher_amt = str(200)
    cursor = connection.cursor()
    cursor.execute("Select * From admin Where price Between "+lower_amt+" And "+higher_amt)
    result = cursor.fetchall()
    return render_template("fruits.html", products=result)

@app.route("/dairy")
def view_dairy():
    lower_amt = str(51)
    higher_amt = str(100)
    cursor = connection.cursor()
    cursor.execute("Select * From admin Where price Between "+lower_amt+" And "+higher_amt)
    result = cursor.fetchall()
    return render_template("dairy.html", products=result)

@app.route("/meat")
def view_meat():
    lower_amt = str(201)
    higher_amt = str(500)
    cursor = connection.cursor()
    cursor.execute("Select * From admin Where price Between "+lower_amt+" And "+higher_amt)
    result = cursor.fetchall()
    return render_template("meat.html", products=result)

@app.route("/usersearch",methods=['GET', 'POST'])
def user_search():
    cursor = connection.cursor()
    if request.method == 'POST':
        getproductname = request.form["pname"]
        cursor.execute("select * from admin where product_name= '" + getproductname + "'")
        result = cursor.fetchall()
        if result is None:
            print("product does not exists ")
        else:
            return render_template("searchproducts.html", search=result, status=True)
    else:
        return render_template("searchproducts.html", search=[], status=False)


@app.route("/cart")
def User_cart():
    try:
        getPid = request.args.get('id')
        getUid = Uid
        cursor = connection.cursor()
        cursor.execute("insert into wrap(admin_product_id,user_id) values("+getPid+",'"+getUid+"')")
        cursor.execute("insert into buy(admin_product_id,user_id) values(" + getPid + ",'" + getUid + "')")
        connection.commit()
        print("Products added to cart successfully")

    except Exception as err:
        print(err)
    return redirect('/cartview')

@app.route("/cartview")
def User_cart_View():
    global getUid ,Uid
    try:
        getUid = Uid
        cursor = connection.cursor()
        cursor.execute("select * FROM admin a join wrap w on w.admin_product_id=a.id where w.user_id="+getUid)
        result = cursor.fetchall()
        cursor.execute("select sum(price) as price from admin a join wrap w on w.admin_product_id = a.id where w.user_id="+getUid)
        result1 = cursor.fetchall()
        cursor.execute("select * FROM admin a join buy b on b.admin_product_id=a.id where b.user_id=" + getUid)
        resultbuy = cursor.fetchall()
        cursor.execute(
            "select sum(price) as price from admin a join buy b on b.admin_product_id = a.id where b.user_id=" + getUid)
        resultbuy1 = cursor.fetchall()
        for i in result1:
            print(i[0])
        return render_template("cartview.html",wrap=result,total=result1,status=True)

    except Exception as err:
        print(err)
    return render_template("cartview.html",wrap=[],status=False)

@app.route("/deletecart",methods=['GET','POST'])
def delete_cart():
    try:
        getPid = request.args.get('id')
        Uid = str(session["id"])
        getUid = Uid
        cursor = connection.cursor()
        cursor.execute("delete from wrap where admin_product_id=" + getPid + " and user_id='" + getUid + "'")
        connection.commit()
        print("Product deleted from cart")

    except Exception as err:
        print(err)
    return redirect('/cartview')

@app.route("/viewexpand")
def View_expand():
    getid = request.args.get('id')
    cursor = connection.cursor()
    cursor.execute("select * from admin where id="+getid)
    result = cursor.fetchall()
    return render_template("viewexpand.html",product=result)

@app.route('/usercheckout')
def user_checkout():
    return render_template("checkout.html")

@app.route('/finalcheckout')
def user_finalcheckout():
    Uid = str(session["id"])
    getUid = Uid
    cursor = connection.cursor()
    cursor.execute("delete from wrap where user_id=" + getUid)
    connection.commit()
    print("Cart cleared sucessfully")
    return redirect("/payment")

@app.route("/payment")
def user_payment():
    return render_template("payment.html")

# @app.route("/pay",methods=["POST"])
# def pay():
#     global payment , name
#     name = request.form.get("username")
#     client = razorpay.Client(auth=("rzp_test_6CbnsHoTB6FPPT","BAvPHiEWU2akNPN3l8odirVe"))
#
#     data = {"amount": 500, "currency": "INR", "receipt": "order_rcptid_11"}
#     payment = client.order.create(data=data)
#     return render_template()
@app.route("/order")
def Order_placed():
    try:
        getUid = Uid
        cursor = connection.cursor()
        cursor.execute("select * FROM admin a join buy b on b.admin_product_id=a.id where b.user_id="+getUid)
        resultbuy = cursor.fetchall()
        # cursor.execute("select sum(price) as price from admin a join buy b on b.admin_product_id = a.id where b.user_id="+getUid)
        # resultbuy1 = cursor.fetchall()
        # for i in resultbuy1:
        #     print(i[0])
        return render_template("order.html",order=resultbuy,status=True)

    except Exception as err:
        print(err)
    return render_template("order.html",order=[],status=False)

@app.route("/tracking")
def view_track():
    return render_template("tracking.html")




if __name__ == "__main__":
    app.run(debug=True)