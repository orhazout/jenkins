from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_cors import CORS
import psycopg2
import json
import os 


app = Flask(__name__)
app.config['SECRET_KEY'] = "my is secret key"
CORS(app)

db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', '5432')
db_name = os.environ.get('DB_NAME', 'postgres')
db_user = os.environ.get('DB_USERNAME', 'postgres')
db_password = os.environ.get('DB_PASSWORD', 'secretpassword')

def create_connection():
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    return conn

def connect_db():
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()

        # Create the users table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR,
                       weight_value INTEGER,
                       mytime TIMESTAMP
            )
        """)
        conn.commit()

        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None


class NameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    weight = StringField("Weight", validators=[DataRequired()])
    time = StringField("Time", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def home():
    return render_template('page.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    conn = connect_db()
    cur = conn.cursor()

    name = None
    form = NameForm()
    if form.validate_on_submit():
        pets = None
        if pets is None:
            cur.execute("INSERT INTO pets (name, weight_value, mytime) VALUES (%s, %s, %s)", (form.name.data, form.weight.data, form.time.data))
            conn.commit()
            cur.close()
            conn.close()
        name = form.name.data
        form.name.data = ''
        form.weight.data = ''
        form.time.data = ''
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pets")
    our_pets= cur.fetchall()
    cur.close()
    conn.close()
    return render_template("data.html", form = form, name = name, our_pets=our_pets)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = create_connection()
    cur = conn.cursor()
    name=None
    cur.execute("SELECT * FROM pets")
    name_to_update= cur.fetchall()
    form = NameForm()
    for pet in name_to_update:
        if form.validate_on_submit():
            try:
                conn = create_connection()
                cur = conn.cursor()    
                cur.execute("UPDATE pets SET name = %s, weight_value = %s, mytime = %s WHERE id = %s;", (form.name.data, form.weight.data, form.time.data, pet[0]))
                conn.commit()
                cur.close()
                conn.close()
                flash("Pet update Successfuly! ")
                name = form.name.data
                return render_template("update.html", form=form, name=name, pet=pet)
            except:
                flash("update failed... try again! ")
                cur.close()
                conn.close()
                return render_template("update.html", form=form, pet=pet)
        else:
            return render_template("update.html", form=form, pet=pet)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)