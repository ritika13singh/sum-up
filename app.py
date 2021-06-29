from flask import Flask, render_template, request, flash, session, redirect

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, request, render_template

import storage

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8znxec]/'

@app.route('/summarizer')
def my_form():
    return render_template('summarizer.html')

@app.route('/logout')
def logout():
    session.pop('username', default=None)
    return redirect("/", code=303)

'''
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text
'''
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        
        if session.get('username') is not None:
            return redirect('home',code=303)
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('uname')
        if not storage.does_user_exist(username):
            flash ("Incorrect login credentials, please try again")
            return render_template('login.html')
        (user_id, user_email, user_password) =  \
        storage.get_user_details(username)
        
        if not check_password_hash (user_password, request.form.get('psw')):
            flash ("Incorrect login credentials, please try again")
            return render_template('login.html')
      
        session['username'] = username
        session.permanent = True if request.form.get('remember') \
                is not None else None

        return redirect('home',code=303)
        

@app.route('/home')
def home():
    if session.get('username') is None:
        return redirect('/', code=303)

    summary_list = storage.get_summary_list(session['username'])

    for index in range(len(summary_list.copy())):
        words = summary_list[index][1].split()[:2]
        heading = words[0] + ' ' + words[1]
        summary_list[index] = (summary_list[index][0], \
                summary_list[index][1], heading)

    username,_,_ = session.get('username').partition("@")
    return render_template('summary-list.html', \
            user=username, summary_list=summary_list)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        if storage.does_user_exist(request.form.get("email")):
            flash ("this email is already in use, please try something else", 'error')
            return render_template('register.html')

        if request.form.get('psw-repeat') != request.form.get('psw'):
            flash ("Passwords didn't matched, please try again", 'error')
            return render_templates('register.html')

        password_hash = generate_password_hash(request.form.get('psw'))
        storage.add_user(request.form.get('email'), 
                         request.form.get('email'),
                         password_hash)
        flash ("Registeration Succesful!")
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug = True)



'''
RISHABH'S app.py
from flask import Flask, redirect, request, render_template
import storage

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login')
def login():
    return "login"

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        if storage.does_user_exist(request.form.get("username")):
            return render_template('register.html', registrationFailed=True)
        else:
            storage.add_user(request.form.get("username"), 
                             request.form.get("email"),
                             request.form.get("password"))
            return "Thank you for registering, " + request.form.get("username") + "!"

@app.route('/profile')
def profile():
    return render_template('profile.html', name='rishabh')

@app.route('/create')
def create_summary():
    return "create summary"
'''
