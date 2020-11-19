from app import app
from app.secviews import requires_auth
import os
from flask import Flask, render_template, flash


@app.route("/")
@requires_auth
def index():
        #flash('Erfolgreich eingeloggt')
        return render_template("public/home.html")

@app.route("/dashboard")
@requires_auth
def dashboard():
        #flash('Erfolgreich eingeloggt')
        userinfo = {
                "team": "Pepegas",
                "pushup_today": 9,
                "pushup_month": 56
        }
        return render_template("public/dashboard.html", userinfo=userinfo)

@app.route("/moin") 
@requires_auth
def home_view(): 
        moin = os.getenv("BASE_URL")
        return f"LOL VAR: {moin}"
        #return "<h1>Welcome to Geeks for Geeks</h1>"