import os
from flask import Flask, request, render_template, redirect, make_response, session, g, url_for, flash, Response, send_from_directory
import sqlite3
from datetime import timedelta
import datetime
import time
import pathlib
import hashlib
from celery import Celery
from redis import Redis

# Initialize Redis connection
redis_client = Redis(host='localhost', port=6379, db=0)


# """
# from celery_config import celery_init_app
# from celery import shared_task, Celery, Task
# from celery.result import AsyncResult
# """

from blueprint_login import bp1
from blueprint_index import bp2
from blueprint_info import bp3
from blueprint_ds import bp6
from blueprint_ds_1st import bp7
from gen_folder import gen_folder

flask_app = Flask(__name__)
flask_app.secret_key ='audz5740dckj'
flask_app.permanent_session_lifetime = timedelta(days=2)
DATABASE = '/home/sahaj/Downloads/Neu/datenbank/user_data.db'

UPLOAD_FOLDER = "/home/sahaj/Downloads/Neu/uploads/" 
flask_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

celery_app = Celery(flask_app.name, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
# """
# flask_app.config.from_mapping(
#     CELERY=dict(
#         broker_url="redis://localhost",
#         result_backend="redis://localhost",
#         task_ignore_result=False,
#     ),
# )
# celery_app = celery_init_app(flask_app)
# """

# Blueprints
flask_app.register_blueprint(bp1, url_prefix='/')
flask_app.register_blueprint(bp7, url_prefix='/')
flask_app.register_blueprint(bp2, url_prefix='/index_page_bp')
flask_app.register_blueprint(bp3, url_prefix='/info_page')
flask_app.register_blueprint(bp6, url_prefix='/ds_page')


redis_client = Redis(host='localhost', port=6379, db=0)

@celery_app.task(bind=True)
def process_large_file_upload(self, user, select, files):
    try:
        folder = gen_folder(user, select)
        for file in files:
            # Save file to disk
            with open(os.path.join(flask_app.config['UPLOAD_FOLDER'], folder.path3_1, file['filename']), 'wb') as f:
                f.write(file['data'])
        return True
    except Exception as e:
        return str(e)



# Database connection (german word for database: "Datenbank") 
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@flask_app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Main page (Home)
@flask_app.route('/index_page', methods=['GET','POST']) 
def index():
    print("Index")
    
    # Check if the user logged in or not?
    if 'user' in session:
        user= session['user']
        print(user)              
    else:
        return render_template("login_page.html")
    
    
    # Select the project (show inside the HTML select tag)
    c = get_db().cursor()
    
    c.execute("SELECT * FROM users WHERE name = ?", [user])
    result = c.fetchall()

    p1 = "-"
    p2 = "-"
    p3 = "-"
    p4 = "-"
    p5 = "-"

    for res in result:
        p1 = res[4] 
        p2 = res[5]
        p3 = res[6]
        p4 = res[7]
        p5 = res[8]
    
    if p1 is None:
        p1 = "-"
    if p2 is None:
        p2 = "-"
    if p3 is None:
        p3 = "-" 
    if p4 is None:
        p4 = "-"   
    if p5 is None:
        p5 = "-"
        
    c.close()    
    
    return render_template('index_page.html', p_1=p1, p_2=p2, p_3=p3, p_4=p4, p_5=p5)


@flask_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True       
        nameinput = request.form['username']
        passwordinput = request.form['password']
        session['user']= nameinput
 
        # Password Hash
        m = hashlib.sha256()
        m.update(passwordinput.encode())
        password_hash = m.hexdigest()
        
        #Input matching with SQL Database. Are the user and the password correct?      
        c = get_db().cursor()
  
        c.execute("SELECT * FROM users WHERE name = ?", [nameinput])     
        c.execute("SELECT * FROM users WHERE password = ?", [password_hash]) 
        result1 = c.fetchone()          

        if result1 == None:
            title_login = "Incorrect input! Please try again."
            return render_template('/login_page.html', l1=title_login)
       
        else:
            
            # Check if the privacy policy (Pp) has been accepted at the first login from the user (needed for switch the pages)
            # ds_check = ds is the abbreviation for the german word "Datenschutz" thats means privacy. 
            user_get = session.get('user')
            
            c.execute("SELECT ds_check FROM users WHERE name =?", [user_get])
            result2 = c.fetchall()

            for res1 in result2:      
                r7 = res1[0]
            
            # The Pp has not been accepted until now. Switch to Pp page.
            r7 = request.form.get('r7')
            if r7 is None:
                return render_template('ds_page_1st.html')
            
            else:
                # The Pp has already been accepted. Pass to main page.       
                c.close()
                return redirect(url_for('index'))        
        
    return render_template('index_page.html')


@flask_app.route('/logout', methods=['GET', 'POST'])
def logout():
    print("logout")
    session.pop('user', None) 
    return render_template('login_page.html')


# This is the route for the  Pp after the first login.
@flask_app.route('/ds_1st_login', methods=['GET', 'POST'])
def ds_1st_login():

    if 'user' in session:
        user= session['user']
        print({user})
    else:
        return render_template("login_page.html")
    
    
    # Check if the Pp has been accepted
    user_get = session.get('user')
    c = get_db().cursor()        
    c.execute("SELECT ds_check FROM users WHERE name =?", [user_get])
    result2 = c.fetchall()

    for res1 in result2:      
        r7 = res1[0]
    
    # Pp has already been accepted
    r7 = request.form.get('r7')
    if r7 is not None:
        c.close()                
        return render_template('index_page.html')
    
    # Pp has not already been accepted    
    else:
        c.close()
 
    
    # The user accepted to the Pp
    if request.method == "POST":
        agree = request.form['ds_agree']

        if agree == "Zustimmen / Agree":
            
            # Set permission to write inside the database
            static_path ="/home/sahaj/Downloads/Neu/datenbank"   
            static_path_check = os.path.isdir(static_path)
        
        
        # If this section runs on the Apache server, I get here an error.
        if static_path_check == True:
                  
            static_path_1 ="/home/sahaj/Downloads/Neu/datenbank/user_data.db" 
            permission = 0o777
            os.chmod(str(static_path_1), permission)
            
            # Generate date when the user accepted to the Pp      
            ds_date = datetime.datetime.now()
            
            c = get_db()
            c.execute("UPDATE users SET ds_check =? WHERE name =?", [ds_date, user])
            c.commit()
            c.close()
            
            # Permission
            static_path ="/home/sahaj/Downloads/Neu/datenbank"
            permission = 0o741
            os.chmod(str(static_path), permission)
            
            return redirect(url_for('index'))
        
        # The user does not accepted to the Pp
        if agree == "Ablehnen / Disagree":
            print("Disagree")
            return redirect(url_for('logout'))
            
    return render_template("ds_page_1st.html")


@flask_app.route('/info', methods=['GET', 'POST'])
def info():

    if 'user' in session:
        user= session['user']
        print({user})
    else:     
        return render_template("login_page.html")


    # Table account information (HTML table tag)
    c = get_db().cursor()

    c.execute("SELECT * FROM users WHERE name = ?", [user])
    result = c.fetchall()

    for res in result:
        r1 = "Username: " 
        r2 = res[0] 
        r3 = "Account creation date: "
        r4 = res[2]
        r5 = "Projects: "
        r6 = res[4] 
        r7 = res[5] 
        r8 = res[6] 
        r9 = res[7] 
        r10 = res[8]
    
    if r6 != None:
        r6_1 = r6 + " |"    
    else:
        r6_1 = ""
    if r7 != None:
        r7_1 = r7 + " |"
    else:
        r7_1 = ""   
    if r8 != None:
        r8_1 = r8 + " |"
    else:
        r8_1 = ""
    if r9 != None:
        r9_1 = r9 + " |"
    else:
        r9_1 = ""
    if r10 != None:
        r10_1 = r10 + " |"
    else:
        r10_1 = ""
              
    c.close()    


    # Change password 
    cpw_title_status =" "
    if request.method == 'POST':    
        try:
            passwordinput2 = request.form['cpw']
            
            # Permission
            static_path ="/home/sahaj/Downloads/Neu/datenbank/user_data.db"
            permission = 0o777
            os.chmod(str(static_path), permission)
            
            # Hash password
            m = hashlib.sha256()
            m.update(passwordinput2.encode())
            password_hash2 = m.hexdigest()          
            
            # Update database
            c = get_db()      
            c.execute("UPDATE users SET password =? WHERE name = ?", (password_hash2, user))
            c.commit()
            c.close()
            
            # Permission
            static_path ="/home/sahaj/Downloads/Neu/datenbank/user_data.db"
            permission = 0o741
            os.chmod(str(static_path), permission)
             
            cpw_title_status = "Your password has changed!"
            
        except:
            print("Except password change")

    return render_template("info_page.html", u1=r1, u2=r2, u3=r3, u4=r4, u5=r5, u6=r6_1, u7=r7_1, u8=r8_1, u9=r9_1, u10=r10_1, cpw=cpw_title_status)
    
# Pp page (Behind the info page)
@flask_app.route('/ds', methods=['GET', 'POST'])
def ds():

    if 'user' in session:
        user= session['user']
        print({user})
    else:
        return render_template("login_page.html")
    
    return render_template('ds_page.html')


@flask_app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        select = request.form['sel_projects']
        username_get = session.get('user')
        files = request.files.getlist("file")

        # Extract relevant file information
        file_data = []
        for file in files:
            file_data.append({
                'filename': file.filename,
                'content_type': file.content_type,
                'data': file.read()  # Read file content as bytes
            })

        # Pass extracted file data to the Celery task
        result = process_large_file_upload.delay(username_get, select, file_data)
        flash("File transfer initiated!", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    flask_app.run(debug=False)



# In addition to the long runnig task, that you will implement in this script, I will create a watch folder(shared_task) to send
# realtime information to the HTML index page (Short technical overview)(EventSource: status_1 and status_2). For example with
# information about the last uploaded file inside the uploads folder and other status informations. I am sill working on that, but
# here are the received session data (user) also important. 

# Thanks for your support. Good luck. 



