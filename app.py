from flask import Flask, render_template, request
import psycopg2

url = "postgres://fdrbblou:HaA31-x3CBhVBXd2FoyrrQv9yygmwh4-@heffalump.db.elephantsql.com/fdrbblou"
app = Flask(__name__)

# Route
@app.route("/")
# Route Handler
def root():
    conn = psycopg2.connect(url)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, email FROM users;")
    # conn.commit()
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('home.html', users=users)


@app.route("/newuser")
# Route Handler
def newuser():
    return render_template('new_user.html')


@app.route("/submit", methods=['POST'])
# Route Handler
def submit():
    username = request.form['username']
    email = request.form['email']

    conn = psycopg2.connect(url)
    cursor = conn.cursor()

    insert_query = "INSERT INTO users (username, email) VALUES (%s, %s)"
    cursor.execute(insert_query, (username, email))

    conn.commit()

    cursor.close()
    conn.close()

    return render_template('new_user.html', username=username, email=email)
