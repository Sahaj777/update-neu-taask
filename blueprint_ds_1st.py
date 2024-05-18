from flask import Blueprint, render_template, redirect

bp7 = Blueprint('bp7',__name__, static_folder='static',template_folder='templates')


@bp7.route('/ds_page_1st')
def ds_page_1st():

    return render_template("ds_page_1st.html")

        
