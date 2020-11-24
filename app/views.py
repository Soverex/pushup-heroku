from app import app
from app.secviews import requires_auth
import os
from flask import Flask, render_template, flash, session, request
import psycopg2

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
def api_data():
        if request.form.get("action") == "addpushup" and request.form.get("user") != "":
                addpushup(request.form.get("user"))
                return{
                        "success" : "true",
                }
        else:
                return {
                        "success" : "false"
                }

def addpushup(user):
    try:
        print(user)
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO \"pushup\" (user_email, datetime, pushup) VALUES ('{user}', current_timestamp, 1);")
        connection.commit()
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")