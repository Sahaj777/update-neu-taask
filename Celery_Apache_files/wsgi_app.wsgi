activate_this = '/var/www/Neu/.venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


import sys

sys.path.insert(0, '/var/www/Neu')


from run2 import flask_app as application

application.secret_key = 'audz5740dckj'




