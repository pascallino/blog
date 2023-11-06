from App import app
from flask import render_template

@app.route('/')
def index():
    name = 'pascal'
    return render_template("index.html", name=name)