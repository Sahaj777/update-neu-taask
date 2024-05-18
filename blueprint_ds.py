from flask import Blueprint, render_template, redirect

bp6 = Blueprint('bp6',__name__, static_folder='static',template_folder='templates')


@bp6.route('/ds_page')
def ds_page():
    return render_template("ds_page.html")


