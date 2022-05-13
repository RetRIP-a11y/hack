import time

from flask import Flask, render_template, request, session, send_from_directory, redirect, url_for
import sqlite3
import hashlib

import docx2txt
import textract
import markText
import base
import idFile
from datetime import date

from werkzeug.utils import secure_filename
import os

import decrypt

app = Flask(__name__, template_folder="templates")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
conn = sqlite3.connect('withOutFace.db', check_same_thread=False)
cur = conn.cursor()

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=('GET', 'POST'))
def index():
    # session['auth'] = False
    session.pop('auth', None)
    return render_template('index.html')

@app.route('/auth', methods=('GET', 'POST'))
def auth():
    # session['auth'] = False
    session.pop('auth', None)
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
            return render_template('index.html')


@app.route('/upload_f', methods=('GET', 'POST'))
def upload():
    text_encr = ''
    text_mark = ''
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'one.doc'))
        key = idFile.add_id_files('one.doc')
        key = "'" + key[6:len(key)-3] + "'"
        userId = "'"+str(session['id'])+"'"
        action = "'" + 'обезличивание' + "'"
        data = "'"+str(date.today())+"'"
        sql = "INSERT INTO process(id_users, key_file, action, date) VALUES ("+userId+', '+key+', '+action+', '+data+");"
        cur.execute(sql)
        conn.commit()
        filename = 'fin.docx'
        try:
            text = docx2txt.process('upload/' + filename)
            text_mark = markText.one(text)
            text_encr = base.markup(text, filename)
        except:
            text = textract.process("upload/" + filename)
            text = text.decode(encoding='utf-8')
            text_mark = markText.one(text)
            text_encr = base.markup(text, filename)
        finally:
            pass
        for string in text_encr[1]:
            keyFile = key
            hash = "'" + str(string[1]) + "'"
            mark = "'" + str(string[2]) + "'"
            word = "'" + str(string[0]) + "'"
            sql1 = "INSERT INTO hash_and_mark(id_process, key_file, hash, mark) VALUES (" + str(000)  + ', ' + keyFile + ', ' + hash + ', ' + mark + ");"
            cur.execute(sql1)
            sql2 = "INSERT INTO data(id_process, string, key_file) VALUES ("+ "'-'" + ', ' + word + ', ' + keyFile +  ");"
            cur.execute(sql2)
            conn.commit()

        return render_template('encrypt.html', content=text_mark, cryptoTxt=text_encr[0])


@app.route('/decrypt_f', methods=('GET', 'POST'))
def decrypt_f():
    text_decrypt = ''
    text = ''
    if request.method == 'POST':
        file = request.files['file']
        filename = 'decrypt.docx'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        key_file = idFile.show_id_files()
        key = "'" + key_file + "'"
        userId = "'" + str(session['id']) + "'"
        action = "'" + 'деобезличивание' + "'"
        data = "'" + str(date.today()) + "'"
        sql = "INSERT INTO process(id_users, key_file, action, date) VALUES (" + userId + ', ' + key + ', ' + action + ', ' + data + ");"
        cur.execute(sql)
        conn.commit()
        key_file = idFile.show_id_files()

        try:
            text = docx2txt.process('upload/' + filename)
            text_decrypt = decrypt.decrypts(text, key_file)
        except:
            text = textract.process("upload/" + filename)
            text = text.decode(encoding='utf-8')
            text_decrypt = decrypt.decrypts(text, key_file)
        finally:
            pass
        return render_template('decrypt.html', content=text, cryptoTxt=text_decrypt)


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('upload/', filename, as_attachment=True)

@app.route('/encrypt', methods=('GET', 'POST'))
def encrypt():
    if 'auth' in session:
        return render_template('encrypt.html')
    else:
        return redirect(url_for('index'))


@app.route('/decrypt', methods=('GET', 'POST'))
def decrypting():
    if 'auth' in session and session['role'] != 'r':
        return render_template('decrypt.html')
    else:
        return redirect(url_for('encrypt'))



@app.route('/page', methods=('GET', 'POST'))
def page():
    if 'auth' in session:
        return render_template('page.html')
    else:
        return redirect(url_for('index'))


@app.route('/root', methods=('GET', 'POST'))
def root():
    if 'auth' in session and session['role'] == 'root':
        return render_template('root.html')
    else:
        return redirect(url_for('encrypt'))


@app.route('/users', methods=('GET', 'POST'))
def users():
    if 'auth' in session and session['role'] == 'root':
        sql = "SELECT * FROM users"
        cur.execute(sql)
        result = cur.fetchall()
        return render_template('users.html', content=result)
    else:
        return redirect(url_for('encrypt'))


@app.route('/delete', methods=('GET', 'POST'))
def delete():
    if 'auth' in session and session['role'] == 'root':
        idForDelete = request.form['dlt_btn']
        sql = "DELETE FROM users WHERE id = " + str(idForDelete) + ";"
        cur.execute(sql)
        conn.commit()
        return redirect(url_for('users'))
    else:
        return redirect(url_for('encrypt'))


@app.route('/create', methods=('GET', 'POST'))
def create():
    if 'auth' in session and session['role'] == 'root':
        new_login = request.form['login']
        new_passsword = hashlib.md5(request.form['password'].encode()).hexdigest()
        new_role = request.form['role']
        sql = "INSERT INTO users(login, password, role) VALUES(" + "'" + new_login + "'" + ', ' + "'" + new_passsword + "'" + ', ' + "'" + new_role + "'" + ");"
        cur.execute(sql)
        conn.commit()
        return redirect(url_for('users'))
    else:
        return redirect(url_for('encrypt'))


@app.route('/logout')
def logout():
    # удаляем имя пользователя из сеанса, если оно есть
    session.pop('auth', None)
    return render_template('index.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=1234)
