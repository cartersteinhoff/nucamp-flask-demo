from flask import Flask, render_template, request, redirect, url_for
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


@app.route("/delete", methods=['POST'])
# Route Handler
def delete():
    email = request.form['email']

    conn = psycopg2.connect(url)
    cursor = conn.cursor()

    # Define the DELETE statement
    delete_query = f"DELETE FROM users WHERE email = '{email}';"
    # Execute the DELETE statement
    cursor.execute(delete_query)
    # Commit the changes to the database
    conn.commit()
    # Close the cursor and the database connection
    cursor.close()
    conn.close()

    return redirect(url_for('root'))
