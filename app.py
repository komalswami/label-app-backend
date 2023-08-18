from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 

@app.route('/generate_zpl', methods=['POST'])
def generate_zpl():
    print("hello world!")
    start = "^XA"
    end = "^XZ"
    label_pos = "^FT"
    label_text_tag = "^FD" 

    change_font = "^CF0,30"
    start_of_field ="^FO"
    end_of_field = "^FS"
    input_text = ['product_code','product_name','customer_code','customer_name']
    input_label = ['product_code','product_name','customer_code','customer_name']

    input_field = "product_name"

    x_start_label = 120 
    y_start_label = 90

    x_start_value = 120 
    y_start_value = 90

    
    y_diff = 30


    for num in range(1, 6):
        print("_____________________________",input_text[num])
        print("******************************",input_label[num])

    #code = start_of_field +str(x)+","+str(y)+label_text_tag+input_text[i]+end_of_field +start_of_field +str(x)+","+str(y)+label_text_tag+input_label[i]+end_of_field  
    total = start + change_font + code +end


    #print(start+label_pos+label_text+input_field+end)
    print(total)


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
    cur.execute("SELECT * FROM labels_table")

    rows = cur.fetchall()

    print("rows",rows)

    conn.close()

    # Convert the results to a list of dictionaries
    columns = [col[0] for col in cur.description]
    list_of_dicts = [dict(zip(columns, row)) for row in rows]

    # Print the list of dictionaries
    for item in list_of_dicts:
        print(item)


    return {"success": True,"data":list_of_dicts}
    #return jsonify({'data':rows}), 200

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
    
    columns = [col[0] for col in cur.description]
    list_of_dicts = [dict(zip(columns, row)) for row in rows]

    conn.close()

    # Print the list of dictionaries
    for item in list_of_dicts:
        print(item)


    return {"success": True,"data":list_of_dicts}

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
    
    columns = [col[0] for col in cur.description]
    list_of_dicts = [dict(zip(columns, row)) for row in rows]

    conn.close()

    # Print the list of dictionaries
    for item in list_of_dicts:
        print(item)


    return {"success": True,"data":list_of_dicts}

if __name__ == '__main__':
    app.run(debug=True,port=4000)