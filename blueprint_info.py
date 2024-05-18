from flask import Blueprint, render_template, redirect

bp3 = Blueprint('bp3',__name__, static_folder='static',template_folder='templates')


@bp3.route('/info_page')
def info_page():
    return render_template("info_page.html")


