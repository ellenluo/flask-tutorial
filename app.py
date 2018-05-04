from flask import Flask, render_template, request, g
import sqlite3

DATABASE = './database.db'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    with app.app_context():
        db = get_db()
        if request.form:
            cur = db.cursor()
            name = request.form.get('name')
            message = request.form.get('message')
            cur.execute("INSERT INTO messages(name, message) VALUES ('{}', '{}')".format(name, message))
            db.commit()
            print(request.form)
        messages = query_db("SELECT * FROM messages")
        print(messages)
        return render_template("home.html", messages=messages)
  
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

if __name__ == '__main__':
    app.run(debug=True)
