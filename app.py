from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app) 

def save_var_list(list_name,input_label):
    conn = sqlite3.connect('database.db') 
    cursor = conn.cursor()
    # store values of label values
    cursor.execute('''CREATE TABLE IF NOT EXISTS label_values (
                      id INTEGER PRIMARY KEY,
                      list_name TEXT,
                      strings TEXT)''')
    strings_str = ';'.join(input_label)  # Convert the list of strings to a semicolon-separated string
    cursor.execute('''INSERT INTO label_values (list_name, strings)
                      VALUES (?, ?)''', (list_name, strings_str))
    conn.commit()

def generate_zpl():
    start = "^XA"
    end = "^XZ"
    label_pos = "^FT"
    label_text_tag = "^FD" 

    change_font = "^CFA,30"
    start_of_field ="^FO"
    end_of_field = "^FS"
    
    data = request.get_json()
    print("****************************************",data)
    is_barcode = data['is_barcode']
    is_qrcode = data['is_qrcode']
    
    input_text = data['label_text']
    input_label = data['label_values']
    
    company_name = data['company_name']
    address = data['company_address']
    
    line_co_ordinates = data['line_co_ordinates']
    
    selected_element_co_text = data['selected_element_co_text']
    selected_element_co_label = data['selected_element_co_label']
    
    rect_co_ordinates = data['rect_co_ordinates']
    
    save_var_list("label1",input_label)

    x_start_label = 80 
    y_start_label = 130

    x_start_value = 350
    y_start_value = 130

    
    y_diff_label = 40
    y_diff_value = 40

    head = start_of_field+str(330) +","+str(20)+label_text_tag+company_name+end_of_field

    code = []
    code.append(start)
    code.append("^CF0,60")
    code.append(head)
    code.append("^CF0,40")
    address = start_of_field+str(360) +","+str(80)+label_text_tag+address+end_of_field
    
    code.append(address)
    code.append("^CFA,30")
    
    input_text_x = []
    input_text_y = []
    input_label_x  = []
    input_label_y = []

    for item in selected_element_co_text:
        if(item is not None):
            #print("***************************************************",item['x1'], item['y1'])
            input_text_x.append(item['x1'])
            input_text_y.append(item['y1'])

    for item in selected_element_co_label:
        if(item is not None):
            #print("********************************************************",item['x1'], item['y1'])
            input_label_x.append(item['x1'])
            input_label_y.append(item['y1'])
    
    line_coordinates_x1 = []
    line_coordinates_y1 = []
    line_coordinates_x2 = []
    line_coordinates_y2 = []

    for item in line_co_ordinates:
        if(item is not None):
            line_coordinates_x1.append(item['x1'])
            line_coordinates_y1.append(item['y1'])
            line_coordinates_x2.append(item['x2'])
            line_coordinates_y2.append(item['y2'])


    for num in range(0, len(input_text)):
        print("_____________________________",input_text[num])
        print("******************************",input_label[num])
        
        #y_start_label = y_start_label+y_diff_label
        #y_start_value = y_start_value + y_diff_value

        #value = input_label[num]
        
        #print("--------------------------------------------------------------------------------",num)
        total_var =start_of_field +str(input_text_x[num])+","+str(input_text_y[num])+label_text_tag+input_text[num]+end_of_field +start_of_field +str(input_label_x[num])+","+str(input_label_y[num])+label_text_tag+ input_label[num] +end_of_field
        #print("-----------------------------  val in for loop----------------------------",total_var)
        code.append(total_var)
    
    items = ""
    #data for barcode
    for num in range(0, len(input_text)):
        item = input_text[num] + ":"+ input_label[num]
        items+= " "+item
    
    
    # y diff = < 5  ----> horizontal line   // y are same    
    # x diff = <5 -------------> vertical line // x are same 

    for num in range(0,len(line_coordinates_x1)):
        if((line_coordinates_x2[num] - line_coordinates_x1[num]) <= 10):              
            # distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            distance = math.sqrt((line_coordinates_x2[num] - line_coordinates_x1[num])**2 + (line_coordinates_y2[num]-line_coordinates_y1[num])**2)
            distance = "1," + str(distance)
            line = "^FO" + str(line_coordinates_x1[num]) + "," + str(line_coordinates_y1[num]) + "^GB"+ distance + ",1" +"^FS" 
            code.append(line)
        else:  
            distance = math.sqrt((line_coordinates_x2[num] - line_coordinates_x1[num])**2 + (line_coordinates_y2[num]-line_coordinates_y1[num])**2)
            distance = str(distance) + ",1"
            line = "^FO" + str(line_coordinates_x1[num]) + "," + str(line_coordinates_y1[num]) + "^GB"+ distance + ",1" +"^FS" 
            code.append(line)
    
    line_coordinates_rect_x1 = []
    line_coordinates_rect_x2 = []
    line_coordinates_rect_y1 = []
    line_coordinates_rect_y2 = []

    for item in rect_co_ordinates:
        if(item is not None):
            print(item)
            line_coordinates_rect_x1.append(item['x1'])
            line_coordinates_rect_x2.append(item['x2'])
            line_coordinates_rect_y1.append(item['y1'])
            line_coordinates_rect_y2.append(item['y2'])
    
    print("line coordinates rect  x1 ",line_coordinates_rect_x1)
    print("line coordinates rect  x2 ",line_coordinates_rect_x2)
    print("line coordinates rect  y1 ",line_coordinates_rect_y1)
    print("line coordinates rect  y2 ",line_coordinates_rect_y2)

    for num in range(0,len(line_coordinates_rect_x1)):
        rectangle = "^FO" + str(line_coordinates_rect_x1[num]) + "," + str(line_coordinates_rect_y1[num]) + "^GB" + str(line_coordinates_rect_x2[num]) + "," + str(line_coordinates_rect_y2[num]) + "^FS"
        print("******************  rectangle *********************** ",rectangle)
        code.append(rectangle)

    if is_barcode == True:
        #zpl with barcode
        barcode =  "^FO"+str(x_start_label)+","+str(y_start_label+y_diff_value)+"^BY3" + "^BCN,100,Y,N,N" + items +"^FS"
        code.append(barcode)
    elif is_qrcode == True:
        barcode =  "^FO"+str(x_start_label)+","+str(y_start_label+y_diff_value)+"^BQN,2,4 ^FDMM"+items +"^FS"
        code.append(barcode)
    else:
        #zpl without qr barcode
        pass

    code.append(end)
    #total = start + change_font + code +end

    delimiter = ','  # Delimiter to be used between elements

    result_string = delimiter.join(code)
    print(result_string)  

    f = open("label1.zpl", "w")
    f.write(result_string)
    f.close()

    return{"success":True}

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