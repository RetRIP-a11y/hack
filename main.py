from flask import Flask, render_template, request
import sqlite3
import hashlib

import textract

from werkzeug.utils import secure_filename
import os

app = Flask(__name__, template_folder="templates")
conn = sqlite3.connect('users.db', check_same_thread=False)
cur = conn.cursor()

UPLOAD_FOLDER = 'upload/test'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html', login='', password='')


@app.route('/check', methods=('GET', 'POST'))
def check():
    if request.method == 'POST':
        login_f = request.form['login']
        password_f = hashlib.md5(request.form['password'].encode()).hexdigest()
        sql = "SELECT * FROM users WHERE login = '" + login_f + "' AND password = '" + password_f + "';"
        cur.execute(sql)
        result = cur.fetchall()
        if result != []:
            id = result[0][0]
            login = result[0][1]
            password = result[0][2]
            role = result[0][3]
            result = {'id': id, 'login': login, 'password': password, 'role': role}
            return render_template('page.html', content=result)
        else:
            return render_template('index.html')


# @app.route('/upload_f', methods=('GET', 'POST'))
# def upload():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # text = textract.process("upload/test/"+filename)
#             # text = text.decode(encoding='utf-8')
#             text = 'GOOD'
#         else:
#             text = 'ERROR'
#         return render_template('page.html', content=text)
@app.route('/upload_f', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
        file = request.files['file']
        text = file
        return render_template('page.html', content=text)

if __name__ == "__main__":
    app.run(debug=True, port=1234)
