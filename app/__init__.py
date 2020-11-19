from flask import Flask, render_template

app = Flask(__name__)

from app import views
from app import secviews

@app.errorhandler(404)
def page_not_found(e):
    return "Not Found | IchBinsTim"