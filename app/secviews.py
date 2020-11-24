from app import app
from app.functions import * 
from flask import Flask, jsonify, redirect, render_template, session
from functools import wraps
import json
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import os
import requests
import psycopg2

app.secret_key = os.getenv("SECRET_KEY")
oauth = OAuth(app)
auth0 = oauth.register('auth0',
    client_id= os.getenv("CLIENTID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    api_base_url=os.getenv("API_BASE_URL"),
    access_token_url=os.getenv("ACCESS_TOKEN_URL"),
    authorize_url=os.getenv("AUTHORIZE_URL"),
    client_kwargs={'scope': 'openid profile email read:appointments',},
)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return render_template('public/home.html')
        return f(*args, **kwargs)
    return decorated

@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    session['jwt_payload'] = userinfo
    session['profile'] = {'user_id': userinfo['sub'],'name': userinfo['name'],'email': userinfo['email'],'picture': userinfo['picture']}
    #CREATE/UPDATE USER IN DB IF NOT EXIST:
    update_database_user(session['profile']['email'],session['profile']['name'])
    updateData()
    return redirect('/')

@app.route('/login')
def login():
    print(os.getenv("BASE_URL"))
    return auth0.authorize_redirect(redirect_uri=f'{os.getenv("BASE_URL")}/callback')

@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': f'{os.getenv("BASE_URL")}', 'client_id': os.getenv("CLIENTID")}
    return redirect('https://soverex.eu.auth0.com/v2/logout?' + urlencode(params))


def update_database_user(email,name):
    try:
        if name == 'Luca':
            team = 'Tim'
        else:
            team = 'Pepegas'
        connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = connection.cursor()
        cursor.execute("INSERT INTO \"USER\" (email, username,team) VALUES (%s, %s,%s) ON CONFLICT (email) DO UPDATE  SET username=%s,team=%s;",(email,name,team,name,team))
        session['team'] = team
        connection.commit()
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")