import time
import zipfile
import magic
from flask import Flask, render_template, request, session, send_from_directory, redirect, url_for
import sqlite3
import hashlib
import docx2txt
import textract
import markText
import base
import idFile
from datetime import date, timedelta
from werkzeug.utils import secure_filename
import os
import decrypt


app = Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(24)
app.config ['portnow_session_lifetime'] = timedelta (days = 365)
conn = sqlite3.connect('withOutFace.db', check_same_thread=False)
cur = conn.cursor()


@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('index.html')


@app.route('/auth', methods=('GET', 'POST'))
def auth():
    return render_template('auth.html')


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
            if role == 'root':
                return redirect(url_for('encrypt'))
            else:
                return redirect(url_for('encrypt'))
        else:
            return redirect(url_for('auth'))


@app.route('/encrypt', methods=('GET', 'POST'))
def encrypt():
    return render_template('encrypt.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=1234)
