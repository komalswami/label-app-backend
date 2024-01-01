from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import numpy as np
from datetime import datetime
import os
from pathlib import Path
from PIL import Image
app = Flask(__name__)
CORS(app) 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

MEDIA_FOLDER = "media"

if not os.path.exists(MEDIA_FOLDER):
    os.makedirs(MEDIA_FOLDER)


MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_FOLDER)

MEDIA_URL = "/media/"


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

# def generate_zpl():
#     start = "^XA"
#     end = "^XZ"
#     label_pos = "^FT"
#     label_text_tag = "^FD" 

#     change_font = "^CFA,30"
#     start_of_field ="^FO"
#     end_of_field = "^FS"
    
#     data = request.get_json()
#     print("****************************************",data)
#     is_barcode = data['is_barcode']
#     is_qrcode = data['is_qrcode']
    
#     input_text = data['label_text']
#     input_label = data['label_values']
    
#     company_name = data['company_name']
#     address = data['company_address']
    
#     line_co_ordinates = data['line_co_ordinates']
    
#     selected_element_co_text = data['selected_element_co_text']
#     selected_element_co_label = data['selected_element_co_label']
    
#     rect_co_ordinates = data['rect_co_ordinates']
    
#     save_var_list("label1",input_label)

#     x_start_label = 80 
#     y_start_label = 130

#     x_start_value = 350
#     y_start_value = 130

    
#     y_diff_label = 40
#     y_diff_value = 40

#     head = start_of_field+str(330) +","+str(20)+label_text_tag+company_name+end_of_field

#     code = []
#     code.append(start)
#     code.append("^CF0,60")
#     code.append(head)
#     code.append("^CF0,40")
#     address = start_of_field+str(360) +","+str(80)+label_text_tag+address+end_of_field
    
#     code.append(address)
#     code.append("^CFA,30")
    
#     input_text_x = []
#     input_text_y = []
#     input_label_x  = []
#     input_label_y = []

#     for item in selected_element_co_text:
#         if(item is not None):
#             #print("***************************************************",item['x1'], item['y1'])
#             input_text_x.append(item['x1'])
#             input_text_y.append(item['y1'])

#     for item in selected_element_co_label:
#         if(item is not None):
#             #print("********************************************************",item['x1'], item['y1'])
#             input_label_x.append(item['x1'])
#             input_label_y.append(item['y1'])
    
#     line_coordinates_x1 = []
#     line_coordinates_y1 = []
#     line_coordinates_x2 = []
#     line_coordinates_y2 = []

#     for item in line_co_ordinates:
#         if(item is not None):
#             line_coordinates_x1.append(item['x1'])
#             line_coordinates_y1.append(item['y1'])
#             line_coordinates_x2.append(item['x2'])
#             line_coordinates_y2.append(item['y2'])


#     for num in range(0, len(input_text)):
#         print("_____________________________",input_text[num])
#         print("******************************",input_label[num])
        
#         #y_start_label = y_start_label+y_diff_label
#         #y_start_value = y_start_value + y_diff_value

#         #value = input_label[num]
        
#         #print("--------------------------------------------------------------------------------",num)
#         total_var =start_of_field +str(input_text_x[num])+","+str(input_text_y[num])+label_text_tag+input_text[num]+end_of_field +start_of_field +str(input_label_x[num])+","+str(input_label_y[num])+label_text_tag+ input_label[num] +end_of_field
#         #print("-----------------------------  val in for loop----------------------------",total_var)
#         code.append(total_var)
    
#     items = ""
#     #data for barcode
#     for num in range(0, len(input_text)):
#         item = input_text[num] + ":"+ input_label[num]
#         items+= " "+item
    
    
#     # y diff = < 5  ----> horizontal line   // y are same    
#     # x diff = <5 -------------> vertical line // x are same 

#     for num in range(0,len(line_coordinates_x1)):
#         if((line_coordinates_x2[num] - line_coordinates_x1[num]) <= 10):              
#             # distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
#             distance = math.sqrt((line_coordinates_x2[num] - line_coordinates_x1[num])**2 + (line_coordinates_y2[num]-line_coordinates_y1[num])**2)
#             distance = "1," + str(distance)
#             line = "^FO" + str(line_coordinates_x1[num]) + "," + str(line_coordinates_y1[num]) + "^GB"+ distance + ",1" +"^FS" 
#             code.append(line)
#         else:  
#             distance = math.sqrt((line_coordinates_x2[num] - line_coordinates_x1[num])**2 + (line_coordinates_y2[num]-line_coordinates_y1[num])**2)
#             distance = str(distance) + ",1"
#             line = "^FO" + str(line_coordinates_x1[num]) + "," + str(line_coordinates_y1[num]) + "^GB"+ distance + ",1" +"^FS" 
#             code.append(line)
    
#     line_coordinates_rect_x1 = []
#     line_coordinates_rect_x2 = []
#     line_coordinates_rect_y1 = []
#     line_coordinates_rect_y2 = []

#     for item in rect_co_ordinates:
#         if(item is not None):
#             print(item)
#             line_coordinates_rect_x1.append(item['x1'])
#             line_coordinates_rect_x2.append(item['x2'])
#             line_coordinates_rect_y1.append(item['y1'])
#             line_coordinates_rect_y2.append(item['y2'])
    
#     print("line coordinates rect  x1 ",line_coordinates_rect_x1)
#     print("line coordinates rect  x2 ",line_coordinates_rect_x2)
#     print("line coordinates rect  y1 ",line_coordinates_rect_y1)
#     print("line coordinates rect  y2 ",line_coordinates_rect_y2)

#     for num in range(0,len(line_coordinates_rect_x1)):
#         rectangle = "^FO" + str(line_coordinates_rect_x1[num]) + "," + str(line_coordinates_rect_y1[num]) + "^GB" + str(line_coordinates_rect_x2[num]) + "," + str(line_coordinates_rect_y2[num]) + "^FS"
#         print("******************  rectangle *********************** ",rectangle)
#         code.append(rectangle)

#     if is_barcode == True:
#         #zpl with barcode
#         barcode =  "^FO"+str(x_start_label)+","+str(y_start_label+y_diff_value)+"^BY3" + "^BCN,100,Y,N,N" + items +"^FS"
#         code.append(barcode)
#     elif is_qrcode == True:
#         barcode =  "^FO"+str(x_start_label)+","+str(y_start_label+y_diff_value)+"^BQN,2,4 ^FDMM"+items +"^FS"
#         code.append(barcode)
#     else:
#         #zpl without qr barcode
#         pass

#     code.append(end)
#     #total = start + change_font + code +end

#     delimiter = ','  # Delimiter to be used between elements

#     result_string = delimiter.join(code)
#     print(result_string)  

#     f = open("label1.zpl", "w")
#     f.write(result_string)
#     f.close()

#     return{"success":True}

def generate_zpl():
    start = "^XA"
    end = "^XZ"
    label_pos = "^FT"
    label_text_tag = "^FD" 
    change_font = "^CFA,30"
    start_of_field ="^FO"
    end_of_field = "^FS"
    data = request.get_json()
    print("****************************************")

    input_labels = data['input_labels']
    text_values_co_ords = data['text_values_co_ords']

    input_qr_code = data['input_qr_code']
    input_barcode = data['input_barcode']
    
    barcode_cords = data['barcode_cords']
    qr_code_cords = data['qr_code_cords']

    line_co_ordinates = data['line_co_ordinates']
    
    rect_co_ordinates = data['rect_co_ordinates']
    font_size = data['font_size']

    font_weight = data['fontweight_array']
    
    image_data = data['image_data']

    #save_var_list("label1",input_labels)

    code = []
    
    code.append(start)
    
    input_text_x = []
    input_text_y = []
    input_label_x  = []
    input_label_y = []
    
    line_coordinates_x1 = []
    line_coordinates_y1 = []
    line_coordinates_x2 = []
    line_coordinates_y2 = []
    line_angle = []

    for item in line_co_ordinates:
        if(item is not None):
            line_coordinates_x1.append(item['x1'])
            line_coordinates_y1.append(item['y1'])
            line_coordinates_x2.append(item['x2'])
            line_coordinates_y2.append(item['y2'])
            line_angle.append(item['angle'])

    text_cords_x1 = []
    text_cords_y1 = []

    for item in text_values_co_ords:
        if(item is not None):
            text_cords_x1.append(item['x1'])
            text_cords_y1.append(item['y1'])
    
    font_style =[]
    for num in range(0, len(input_labels)):
        if(font_weight[num]=='bold'):
            font_style.append('^CF0')
        else:
            font_style.append('^AN')

    for num in range(0, len(input_labels)):
        total_var =font_style[num]+','+str(font_size[num])+ start_of_field +str(text_cords_x1[num])+","+str(text_cords_y1[num])+label_text_tag+input_labels[num]+end_of_field
        code.append(total_var)
    
    for num in range(0,len(line_coordinates_x1)):
        if(line_angle[num]>0 and line_angle[num]<175 or line_angle[num]>263 and line_angle[num]<280):
            line = "^FO" + str(line_coordinates_x1[num]) + "," + str(line_coordinates_y1[num]) + "^GB"+"1," +str(line_coordinates_x2[num]) +"^FS"
            code.append(line)
        else:
            line = "^FO" + str(line_coordinates_x1[num]) + "," + str(line_coordinates_y1[num]) + "^GB"+ str(line_coordinates_x2[num]) + ",1" +"^FS" 
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
    
    for num in range(0,len(line_coordinates_rect_x1)):
        rectangle = "^FO" + str(line_coordinates_rect_x1[num]) + "," + str(line_coordinates_rect_y1[num]) + "^GB" + str(line_coordinates_rect_x2[num]) + "," + str(line_coordinates_rect_y2[num]) + "^FS"
        code.append(rectangle)

    barcode_cords_x1 = ''
    barcode_cords_y1 = ''
    barcode_cords_width = ''

    for item in barcode_cords:
        if(item is not None):
            barcode_cords_x1 = item['x1']
            barcode_cords_y1 = item['y1']
            barcode_cords_width = item['width']
    
    qr_code_cords_x1 = ''
    qr_code_cords_y1 = ''

    for item in qr_code_cords:
        if(item is not None):
            qr_code_cords_x1 = item['x1']
            qr_code_cords_y1 = item['y1']

    if input_barcode!=' ' and  input_barcode:
        #zpl with barcode
        print("********************************************",input_barcode)
        barcode =  "^FO"+str(barcode_cords_x1)+","+str(barcode_cords_y1)+"^BY3" + "^BCN,"+str(barcode_cords_width)+",Y,N,N" + input_barcode +"^FS"
        code.append(barcode)
    elif input_qr_code!=' ' and  input_qr_code:
        qr_code =  "^FO"+str(qr_code_cords_x1)+","+str(qr_code_cords_y1)+"^BQN,2,3 ^FDMM00"+ input_qr_code +"^FS"
        code.append(qr_code)
    else:
        #zpl without qr barcode
        pass

    logo_flag = data['logo_flag']
    img_x1 = 0
    img_y1 = 0

    for item in image_data:
        if(item is not None):
            img_x1 = item['x1']
            img_y1 = item['y1']
    
    #start
    zpl_command =''
    if(logo_flag==True):
        image = Image.open(data['file_path'])
        print("filepath",data['file_path'])
        width = 200  # Desired width in dots
        height = 200  # Desired height in dots
        image = image.resize((width, height), Image.ANTIALIAS)

        # Convert the image to grayscale
        image = image.convert('L')
        image = image.point(lambda x: 0 if x >= 128 else 1, '1')

        # Initialize the ZPL command string
        zpl_command = "^FO"+str(img_x1)+","+str(img_y1)+"^GFA,{0},{1},{2},".format(
            width, height*25, width // 8
        )

        # Convert the image data to ZPL format
        for y in range(0, height):
            for x in range(0, width // 8):
                byte = 0
                for i in range(8):
                    pixel = image.getpixel((x * 8 + i, y))
                    byte |= (pixel & 1) << (7 - i)
                zpl_command += "{:02X}".format(byte)

        # Close the ZPL command string
        zpl_command += "^FS"
    
        # Print or save the ZPL command string as needed
        print(zpl_command)

    #end

    code.append(zpl_command)
    code.append(end)
    #total = start + change_font + code +end

    delimiter = ','  # Delimiter to be used between elements

    result_string = delimiter.join(code)
    print(result_string)  
    
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    fname = f"{MEDIA_FOLDER}/Label_{ts}.zpl"
    
    f = open(fname, "w")
    f.write(result_string)
    f.close()
        
    return{"success": True, "file_path": fname}

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