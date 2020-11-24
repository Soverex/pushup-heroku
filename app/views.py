from app import app
from app.secviews import requires_auth
from app.functions import * 
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
        updateData()
        userinfo = {
                "team": session['team'],
                "pushup_today": session['pushup_day'],
                "pushup_month": session['pushup_all'], 
                "pushup_gegner": session['pushup_gegner'], 
                "pushup_team": session['pushup_team'], 
        }
        return render_template("public/dashboard.html", userinfo=userinfo)
        

@app.route("/pushup") 
@requires_auth
def pushup(): 
        return render_template("public/pushup.html", base=os.getenv("BASE_URL"), user_mail=session['profile']['email'])

@app.route("/statistics") 
@requires_auth
def statistics(): 
        return render_template("public/statistics.html")

@app.route("/admin") 
@requires_auth
def admin(): 
        return render_template("public/admin.html")

@app.route("/api/data", methods=['POST']) 
@requires_auth
def api_data():
        if request.form.get("action") == "addpushup" and request.form.get("user") != "":
                addpushup(request.form.get("user"))
                data = getpushup_data(request.form.get("user"))
                session['pushup_day'] = data
                return{
                        "success" : "true",
                        "data"    : f"{data}"
                }
        else:
                return {
                        "success" : "false"
                }