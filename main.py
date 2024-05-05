from flask import Flask, render_template, redirect, request, session
import sqlite3
import os


################### Database Setup #########################
DATABASE_NAME = "database/Thoab_Al6alb.db"


def db_control(query, fetch=True):
    connection = sqlite3.connect(DATABASE_NAME)
    cur = connection.cursor()
    cur.execute(query)
    if fetch:
        result = cur.fetchall()
        connection.close()
        return result
    connection.commit()
    connection.close()


################### Create Flask APP  #########################

app = Flask(__name__)
app.secret_key = "Thoab_Al6alb"


# Home Page Route
@app.route("/")
def home():
    user_email = session.get("user_email", None)
    return render_template("index.html", email=user_email)


# showbook Page Route
@app.route("/signin")
def login():
    msg = session.pop("msg", None)
    user_email = session.get("user_email", None)
    return render_template("login.html", msg=msg, email=user_email)


# showbook Page Route
@app.route("/signup")
def rejester():
    msg = session.pop("msg", None)
    user_email = session.get("user_email", None)
    return render_template("rejster.html", msg=msg, email=user_email)


# select catogry Page Route
@app.route("/selectcatogry")
def select_catogry():
    user_email = session.get("user_email", None)
    if user_email == None:
        return redirect("/signin")
    return render_template("selectcatogry.html", email=user_email)


# add book Page Route
@app.route("/addbook-col")
def add_book_col():
    user_email = session.get("user_email", None)
    if user_email == None:
        return redirect("/")
    return render_template(
        "addbookcollege.html", msg=session.pop("msg", None), email=user_email
    )


# add book Page Route
@app.route("/addbook-school")
def add_book_school():
    user_email = session.get("user_email", None)
    if user_email == None:
        return redirect("/")
    return render_template(
        "addbookschool.html", msg=session.pop("msg", None), email=user_email
    )


# showbook Page Route
@app.route("/showbook")
def show_book():
    user_email = session.get("user_email", None)
    result_one = db_control("SELECT * FROM school_books;")
    result_two = db_control(" SELECT * FROM university_books")
    result = [*result_two, *result_one]
    return render_template("showbook.html", email=user_email, data=result)


################### Handel Request  #########################


# add Book For university
@app.route("/addbook-handel-col", methods=["POST"])
def addbook_handel():
    data = request.form
    book_name = data.get("book_name", None)
    specialization_name = data.get("dep_name", None)
    college_name = data.get("col_name", None)
    college_team = data.get("tem_name", None)
    mobile_number = data.get("user_phone", None)
    address = data.get("user_ad", None)
    file = request.files["img"]
    folder_dir = os.getcwd()
    path = rf"{folder_dir}\static\uplode\{file.filename}"
    file.save(path)
    query = f"""INSERT INTO university_books ( address, book_name, college_name, mobile_number, picture_book, specialization_name, college_team )
                             VALUES ( '{address}', '{book_name}', '{college_name}', '{mobile_number}', '{file.filename}', '{specialization_name}', '{college_team}' );"""
    db_control(query, fetch=False)
    session["msg"] = "تم أَضافة الكتاب بنجاح"
    return redirect("/addbook-col")


# add Book For School
@app.route("/addbook-handel-school", methods=["POST"])
def addbook_handel_school():
    data = request.form
    book_name = data.get("book_name", None)
    level_study = data.get("level_study", None)
    study_year = data.get("study_year", None)
    trem_number = data.get("trem_number", None)
    user_address = data.get("user_address", None)
    user_phone = data.get("user_phone", None)
    file = request.files["book_img"]
    folder_dir = os.getcwd()
    path = rf"{folder_dir}\static\uplode\{file.filename}"
    file.save(path)
    query = f""" INSERT INTO school_books (  level_study, study_year, trem_number, book_name, user_address, user_phone, book_img)
                             VALUES ( '{level_study}', '{study_year}', '{trem_number}', '{book_name}', '{user_address}', '{user_phone}', '{file.filename}' );"""
    db_control(query, fetch=False)
    session["msg"] = "تم أَضافة الكتاب بنجاح"
    return redirect("/addbook-school")


# Register Handel
@app.route("/handel-register", methods=["POST"])
def handel_register():
    data = request.form
    user_name = data.get("user_name", None)
    user_phone = data.get("user_phone", None)
    user_email = data.get("user_email", None)
    user_password = data.get("user_password", None)
    query = f"""SELECT email FROM users WHERE email = '{user_email}'"""
    result = db_control(query)
    if len(result) == 0:
        query = f"""INSERT INTO users ( name , email, pass, phone ) VALUES (  '{user_name}' ,  '{user_email}' ,  '{user_password}' , {user_phone});"""
        db_control(query, fetch=False)
        return redirect("/signin")
    else:
        msg = "الـبريد الالكترونى موجود بالفعل"
        session["msg"] = msg
        return redirect("/signup")


# Login Handel
@app.route("/handel-login", methods=["POST"])
def handel_login():
    data = request.form
    email = data.get("userEmail", None)
    password = data.get("userPassword", None)
    query = f"""SELECT email , pass FROM users WHERE email = '{email}'"""
    result = db_control(query)
    if len(result) != 0:
        if result[0][0] == email and result[0][1] == password:
            session["user_email"] = email
            return redirect("/")
        else:
            msg = "الـبريد الالكترونى او كلمة السر  غير صحيحة "
            session["msg"] = msg
            return redirect("/signin")
    else:
        msg = "الـبريد الالكترونى غير موجود "
        session["msg"] = msg
        return redirect("/signin")


# logo out Function
@app.route("/logout")
def logout():
    session.pop("user_email", None)
    return redirect("/")


################### Run Flask APP  #########################

# python main.py


if __name__ == "__main__":
    app.run(debug=True)
