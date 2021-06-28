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