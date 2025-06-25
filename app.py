import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        import time
        time.sleep(5)
        return get_db_connection()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM f2p_games")
    f2p_games = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', games=f2p_games)

@app.route('/add', methods=['POST'])
def add_game():
    game = request.form['game']
    pengembang = request.form['pengembang']
    konten_dewasa = request.form['konten_dewasa']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO f2p_games (game, pengembang, konten_dewasa) VALUES (%s, %s, %s)", (game, pengembang, konten_dewasa))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit_game(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM f2p_games WHERE id = %s", (id,))
    game = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', game=game)

@app.route('/update/<int:id>', methods=['POST'])
def update_game(id):
    game = request.form['game']
    pengembang = request.form['pengembang']
    konten_dewasa = request.form['konten_dewasa']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE f2p_games SET game = %s, pengembang = %s, konten_dewasa = %s WHERE id = %s",
                   (game, pengembang, konten_dewasa, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_game(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM f2p_games WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)