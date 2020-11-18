from app import app
from app.secviews import requires_auth
import os


@app.route("/")
@requires_auth
def index():
    return "Logged In MO"

@app.route("/moin") 
#@requires_auth
def home_view(): 
        moin = os.getenv("BASE_URL")
        return f"LOL VAR: {moin}"
        #return "<h1>Welcome to Geeks for Geeks</h1>"