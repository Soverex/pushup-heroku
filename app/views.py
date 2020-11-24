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
                data = getpushup_data(request.form.get("user"))
                return{
                        "success" : "true",
                        "data"    : f"{data}",
                }
        else:
                return {
                        "success" : "false"
                }

def addpushup(user):
    try:
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

def getpushup_data(user):
    try:
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute(f"select sum(pushup) from \"pushup\" where user_email = '{user}' and DATE(datetime) >= CURRENT_DATE AND DATE(datetime) < CURRENT_DATE + INTERVAL '1 DAY'")
        result = cursor.fetchone()[0]
        return result
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        return 0
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")