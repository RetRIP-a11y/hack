from flask import Flask, render_template, request
import sqlite3
import hashlib
app = Flask(__name__, template_folder="templates")
conn = sqlite3.connect('users.db', check_same_thread=False)
cur = conn.cursor()


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
            result = {'id':id, 'login':login, 'password':password, 'role':role}
            return render_template('page.html', content=result)
        else:
            return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=1234)
