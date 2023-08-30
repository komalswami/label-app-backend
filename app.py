from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app) 

@app.route('/generate_zpl', methods=['POST'])
def generate_zpl():

    print("hello world!")
    #data = request.get_json()

    #print("hello world!",data)
    start = "^XA"
    end = "^XZ"
    label_pos = "^FT"
    label_text_tag = "^FD" 

    change_font = "^CF0,30"
    start_of_field ="^FO"
    end_of_field = "^FS"
    input_text = ['product_code','product_name','customer_code','customer_name']
    input_label = ['product_code','product_name','customer_code','customer_name']
    
    # is_barcode = data['is_barcode']
    # is_qrcode = data['is_qrcode']
    # input_text = data['label_text']
    # input_label = data['label_values']
    # company_name = data['company_name']
    # address = data['address']'

    company_name = "company name"
    address = "address"

    # ^FO100,100^BY3
    # ^BCN,100,Y,N,N
    # ^FD123456^FS

    is_barcode = False
    is_qrcode = True



    input_field = "product_name"

    x_start_label = 120 
    y_start_label = 90

    x_start_value = 370
    y_start_value = 90

    
    y_diff_label = 30
    y_diff_value = 30

    #start_of_head = "^CF0,60" 
    head = start_of_field+str(x_start_label) +","+str(y_start_label)+start_of_field+company_name+end_of_field

    code = []
    code.append(start)
    code.append(head)

    

    address = start_of_field+str(x_start_label) +","+str(y_start_label)+start_of_field+address+end_of_field

    code.append(head)
    code.append(address)
    code.append(change_font)
    
    for num in range(0, len(input_text)):
        print("_____________________________",input_text[num])
        print("******************************",input_label[num])
        
        y_start_label = y_start_label+y_diff_label
        y_start_value = y_start_value + y_diff_value
        
        # f"{data['total_weight']}"
        ## f"{data[+'input_label[num]+']}"

        value1 = 'f'
        doub = '"'
        value2 = "{data['"
        value3 = """']}"""

        value = value1 + doub + value2 + input_label[num] + value3 + doub
        
        # original_string = 'This is a "{}" word'
        # formatted_string = original_string.format('quoted')
        
        #print(doub)
        print(value)
        total_var =start_of_field +str(x_start_label)+","+str(y_start_label)+label_text_tag+input_text[num]+end_of_field +start_of_field +str(x_start_value)+","+str(y_start_value)+label_text_tag+value+end_of_field
        code.append(total_var)
    
    if is_barcode == True:
        #zpl with barcode
        barcode =  "^FO"+str(x_start_value)+","+str(y_start_value+y_diff_value)+"^BY3" + "^BCN,100,Y,N,N" + "^FD" + "123456" +"^FS"
        code.append(barcode)
    elif is_qrcode == True:
        #^FO100,100^BQN,2,4
        #^FDMM,AAC-42^FS
        barcode =  "^FO"+str(x_start_value)+","+str(y_start_value+y_diff_value)+"^BQN,2,4 ^FDMM,AAC-42" +"^FS"
        code.append(barcode)
    else:
        #zpl without qr barcode
        pass

    code.append(end)
    #total = start + change_font + code +end

    delimiter = ','  # Delimiter to be used between elements

    result_string = delimiter.join(code)
    print(result_string)  # Output: 'apple, banana, cherry'


    f = open("label.zpl", "w")
    f.write(result_string)
    f.close()

    #total = np.array(code)
    #print(start+label_pos+label_text+input_field+end)
    #print(total)

    return{"success":True,"data":result_string }


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

@app.route('/select_units', methods=['GET'])
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

@app.route('/select_date_time', methods=['GET'])
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