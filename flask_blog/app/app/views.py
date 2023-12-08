from App import app
from flask import render_template

@app.route('/')
def index():
    name = 'pascal'
    return render_template("posts/page.html", name=name)