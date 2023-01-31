from base64 import b64encode
from os import environ
from flask import Flask, redirect, request, session
from flask import render_template
from requests import get

import json

underConstruction = True

SELF_URL_AUTH = 'https://uerl-corperation-entities-listing.wolfieboy09.repl.co/authenticate'

app = Flask(__name__)

def base64(string):
    return b64encode(string.encode("utf-8")).decode()

@app.get("/")
def home():
    if "username" in session:
        return redirect('/pannel')
    else:
        return redirect(f"https://auth.itinerary.eu.org/auth/?redirect={ base64(f'{SELF_URL_AUTH}') }&name=U.E.R.L%20Corporation")

@app.get("/authenticate")
def handle():
    privateCode = request.args.get("privateCode")
    if privateCode == None:
        return "Bad Request", 400
    resp = get(f"https://auth.itinerary.eu.org/api/auth/verifyToken?privateCode={privateCode}").json()
    if resp["redirect"] == f"{SELF_URL_AUTH}":
        if resp["valid"]:
            session["username"] = resp["username"]
            return redirect("/")
        else:
            return "Authentication failed - please try again later."
    else:
        return "Invalid Redirect", 400

def getRank(user):
  with open('data/ranks.json', 'r') as f:
    r = json.load(f)
    if user in r['studio']["curators"]:
      return 'curator'
    elif user in r['admin']:
      return 'admin'
    elif user in r['studio']['managers']:
      return 'managers'
    else:
      return 'guest'

@app.route('/under')
def under():
  return render_template('workingOn.html')

@app.route('/test')
def test():
  return render_template('entities/030.html')

@app.route('/pannel')
def pannel():
  if underConstruction is True:
    return redirect('/under')
    username = session["username"]
  return render_template('ent.html', username=username)

@app.route('/entities/{id}')
def loadEntity(id):
  return f"REQUESTED: {id}" 
  
@app.route('/entities', methods=['GET', 'POST'])
def entities():
  return render_template('listing.html', entitys=[{"classified": False, "id":1},{"classified": True, "id":2}])


app.run(host='0.0.0.0', port=4313, debug=True)