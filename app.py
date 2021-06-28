from flask import Flask, render_template, request

from werkzeug.utils import secure_filename

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/summarizer')
def my_form():
    return render_template('summarizer.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text
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