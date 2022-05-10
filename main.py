from flask import Flask, render_template, request, session, send_from_directory, redirect, url_for
import sqlite3
import hashlib

import docx2txt
import textract
import markText
import base

from werkzeug.utils import secure_filename
import os

import test

app = Flask(__name__, template_folder="templates")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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
    session['auth'] = False
    return render_template('index.html')


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
            role = result[0][3]
            session['auth'] = True
            session['role'] = role
            session['id'] = id

            return redirect(url_for('encrypt'))
        else:
            return render_template('index.html')


@app.route('/upload_f', methods=('GET', 'POST'))
def upload():
    text_encr = ''
    text_mark = ''
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                text = docx2txt.process('upload/test/' + filename)
                text_mark = markText.one(text)
                text_encr = base.markup(text, filename)
            except:
                text = textract.process("upload/test/" + filename)
                text = text.decode(encoding='utf-8')
                text_mark = markText.one(text)
                text_encr = base.markup(text)
            finally:
                pass
        return render_template('encrypt.html', content=text_mark, cryptoTxt=text_encr)


@app.route('/decrypt_f', methods=('GET', 'POST'))
def decrypt_f():
    text_encr = ''
    text_mark = ''
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            try:
                text = docx2txt.process('upload/test/' + filename)
                text_decrypt = test.decrypt(text)
            except:
                text = textract.process("upload/test/" + filename)
                text = text.decode(encoding='utf-8')
                text_decrypt = test.decrypt(text)
            finally:
                pass
        return render_template('encrypt.html', content=text, cryptoTxt=text_decrypt)


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('upload/test', filename, as_attachment=True)


@app.route('/encrypt', methods=('GET', 'POST'))
def encrypt():
    if 'auth' in session:
        return render_template('encrypt.html')
    else:
        return render_template('404.html')


@app.route('/decrypt', methods=('GET', 'POST'))
def decrypt():
    if 'auth' in session:
        return render_template('decrypt.html')
    else:
        return render_template('404.html')



@app.route('/page', methods=('GET', 'POST'))
def page():
    if 'auth' in session:
        return render_template('page.html')
    else:
        return render_template('404.html')


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    # удаляем имя пользователя из сеанса, если оно есть
    session.pop('auth', None)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=1234)
