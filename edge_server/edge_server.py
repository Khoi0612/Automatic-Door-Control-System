import serial
import pymysql
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
import threading
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
app = Flask(__name__)

def get_db_connection(host='localhost', user='root', password='12345678', db='doorlog'):
    conn = pymysql.connect(host=host, user=user, password=password, database=db)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            time DATETIME,
            distance FLOAT,
            light INT,
            control VARCHAR(20),
            door VARCHAR(20),
            alarm VARCHAR(20)
        )
    ''')
    conn.commit()
    return conn
    
def log_data():
    while True:
        try:
            if ser.in_waiting:
                line = ser.readline().decode().strip()
                parts = line.split(',')
                dist = float(parts[0].split(':')[1])
                light = int(parts[1].split(':')[1])
                control = parts[2].split(':')[1]
                door = parts[3].split(':')[1]
                alarm = parts[4].split(':')[1]
                now = datetime.now()
                
                conn = get_db_connection()  
                cur = conn.cursor()
                cur.execute("INSERT INTO logs (time, distance, light, control, door, alarm) VALUES (%s, %s, %s, %s, %s, %s)",
                            (now, dist, light, control, door, alarm))
                conn.commit()
                conn.close()
                
                
        except Exception as e:
            print("Error reading from Arduino:", e)
        time.sleep(1)
        
def fetch_latest_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM logs ORDER BY time DESC LIMIT 1")
    data = cur.fetchone()
    return data

    
def fetch_data_column(start_time, end_time, conn, parameter):
    if parameter not in ['distance', 'light', 'control', 'door', 'alarm']:
        raise ValueError("Invalid column requested")

    cur = conn.cursor()
    query = f"SELECT {parameter} FROM logs WHERE time BETWEEN %s AND %s"
    cur.execute(query, (start_time, end_time))
    data = [row[0] for row in cur.fetchall()]
    conn.close()
    return data


def count_customer(door_states):
    count = 0
    for i in range(len(door_states) - 1):
        if door_states[i] == 'Closed' and door_states[i + 1] == 'Open':
            count += 1
    return round(count / 2)

@app.route('/')
def index():
    count = request.args.get('count')
    return render_template('index.html', count=count)

@app.route('/latest-log')
def latest_log():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM logs ORDER BY time DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if row:
        return jsonify({
            'time': row[0].strftime('%Y-%m-%d %H:%M:%S'),
            'distance': row[1],
            'light': row[2],
            'control': row[3],
            'door': row[4],
            'alarm': row[5]
        })
    return jsonify(None)

    
@app.route('/traffic', methods=['GET', 'POST'])
def customer_traffic():
    count = None
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        conn = get_db_connection()
        doors = fetch_data_column(start, end, conn, 'door')
        count = count_customer(doors)
        return redirect(url_for('index', count=count))
    
    return redirect(url_for('index'))

@app.route('/manual-control', methods=['POST'])
def manual_toggle():
    try:
        ser.write(b'manual\n')
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error sending data to Arduino: {e}", 500

@app.route('/door-toggle', methods=['POST'])
def door_toggle():
    try:
        ser.write(b'door\n')
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error sending data to Arduino: {e}", 500
    
@app.route('/alarm-toggle', methods=['POST'])
def alarm_toggle():
    try:
        ser.write(b'alarm\n')
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error sending data to Arduino: {e}", 500


threading.Thread(target=log_data, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)