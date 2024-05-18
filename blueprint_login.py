from flask import Blueprint, render_template, session

bp1 = Blueprint('bp1',__name__, static_folder='static', template_folder="templates")



@bp1.route('/')
def login():
    return render_template("login_page.html")


