from App import app
from flask import render_template
from flask_login import current_user

@app.route('/')
def index():
    if current_user.is_authenticated:
        name = current_user.first_name
    else:
        name = ""
    return render_template("posts/page.html", name=name)