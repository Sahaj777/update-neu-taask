from flask import Blueprint, render_template, session

bp2 = Blueprint('bp2',__name__, static_folder='static',template_folder='templates')



@bp2.route('/index_page')
def index_page():
    return render_template("index_page.html")



