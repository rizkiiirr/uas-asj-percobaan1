# app.py
import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv() # Memuat variabel dari file .env

app = Flask(__name__)

# --- KONEKSI DATABASE ---
# Mengambil konfigurasi database dari environment variables
# Ini memenuhi Syarat 7: Tidak menumpuk data privasi di docker-compose.yml
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
        # Coba lagi setelah beberapa saat jika koneksi gagal (misal: database belum siap)
        import time
        time.sleep(5)
        return get_db_connection()


# --- RUTE APLIKASI (CRUD) ---
# Syarat 1 & 3: Menerapkan CRUD dan terhubung ke database 

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tickets=tickets)

@app.route('/add', methods=['POST'])
def add_ticket():
    nama_tiket = request.form['nama_tiket']
    harga = request.form['harga']
    stok = request.form['stok']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tickets (nama_tiket, harga, stok) VALUES (%s, %s, %s)", (nama_tiket, harga, stok))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit_ticket_view(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets WHERE id = %s", (id,))
    ticket = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', ticket=ticket)

@app.route('/update/<int:id>', methods=['POST'])
def update_ticket(id):
    nama_tiket = request.form['nama_tiket']
    harga = request.form['harga']
    stok = request.form['stok']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET nama_tiket = %s, harga = %s, stok = %s WHERE id = %s",
                   (nama_tiket, harga, stok, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_ticket(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Menjalankan aplikasi dengan host 0.0.0.0 agar bisa diakses dari luar container
    app.run(host='0.0.0.0', port=5000, debug=True)