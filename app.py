from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 

@app.route('/data', methods=['POST'])
def accept_data():
    #data = request.json  # Assuming the data is sent in JSON format
    
    #print(data)
    # Process the data as needed

    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    #conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
    conn.execute('CREATE TABLE units_table (id int, name TEXT)')
    conn.execute('CREATE TABLE date_time_table (id int, date TEXT,time TEXT,datetime TEXT)')
    conn.execute('CREATE TABLE labels_table(id int, name TEXT)')
    

    print("Table created successfully")
    conn.close()
    
    return jsonify({'message': 'Data received successfully'}), 200

@app.route('/select_labels', methods=['GET'])
def select_labels():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    cur = conn.cursor()
    cur.execute("SELECT name FROM labels_table")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()
    
    return jsonify({'data':rows}), 200

@app.route('/select_units', methods=['POST'])
def select_units():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    cur = conn.cursor()
    cur.execute("SELECT name FROM units_table")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()
    
    return jsonify({'data':rows}), 200

@app.route('/select_date_time', methods=['POST'])
def select_date_time():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    cur = conn.cursor()
    cur.execute("SELECT date FROM date_time_table")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()
    
    return jsonify({'data':rows}), 200

if __name__ == '__main__':
    app.run(debug=True,port=4000)