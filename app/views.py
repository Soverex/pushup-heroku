from app import app
from app.secviews import requires_auth
import os
from flask import Flask, render_template, flash, session
import psycopg2

try:
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute('SELECT * FROM "USER"')
    record = cursor.fetchone()
    print(record)
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route("/")
@requires_auth
def index():
        return render_template("public/home.html")

@app.route("/dashboard")
@requires_auth
def dashboard():
        userinfo = {
                "team": "Pepega's",
                "pushup_today": 9,
                "pushup_month": 56
        }
        return render_template("public/dashboard.html", userinfo=userinfo)

@app.route("/pushup") 
@requires_auth
def pushup(): 
        return render_template("public/pushup.html", base=os.getenv("BASE_URL"), user_mail=session['profile']['email'])

@app.route("/api/data", methods=['POST']) 
@requires_auth
def apt_data(): 
        return{
                "success" : "true"
        }
