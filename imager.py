import streamlit as st
from PIL import Image
import pandas as pd
import easyocr
import re
import json
import mysql.connector
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie


res = []  # List to store the results for each uploaded image



# Create empty lists to store the extracted details for each image.
data1 = {'Name':[],"company":[],'Designation':[],'email':[],'primary_number':[],'secondary_number':[],'website':[],'address':[]}

host = "localhost"
port = 3306
user = "root"
password = "Ganesha143@"

# Create a connection object
conn = mysql.connector.connect(host=host, port=port, user=user, password=password)
cursor = conn.cursor()

Db = cursor.execute("USE business_card;")
try:
    cursor.execute("""CREATE TABLE IF NOT EXISTS bz_card(
                    Name VARCHAR(255) NOT NULL UNIQUE,
                    Company VARCHAR(255) NOT NULL,
                    Designation VARCHAR(255) NOT NULL,
                    Email VARCHAR(255) NOT NULL,
                    Primary_Number VARCHAR(255) NOT NULL,
                    Secondary_Number VARCHAR(255),
                    Website VARCHAR(255) NOT NULL,
                    Address VARCHAR(255) NOT NULL,
                    Image VARCHAR(255) NOT NULL
                );""")
except:
  print("Table already exists in database")




# pd.read_sql("drop table bz_card;",conn)
# Define the all_details list as a global variable.
global all_details
# Define the all_details list outside of the Streamlit app.
all_details = []

# Define the image_bytes_dict dictionary.
image_bytes_dict = {}


def upload():
    container = st.container()
    try:
        with container:
            @st.cache_data(ttl=60 * 60)
            def load_lottie_file(filepath : str):
                with open(filepath, "r") as f:
                    gif = json.load(f)
                st_lottie(gif, speed=1, width=800, height=450)
                
            load_lottie_file("upload.json")
    except:
        print("Don't raise exception")

    st.title("Image Uploader")
    st.write("Upload an image and we'll display it below.")
    # que = pd.read_sql("show tables;",conn)
    # st.write(que)
    # Create a file uploader widget
    uploaded_images = st.file_uploader("Choose images...", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    # Iterate over the uploaded images and process each image individually.
    for uploaded_image in uploaded_images:

        # Open the uploaded image.
        image = Image.open(uploaded_image)

        
        # st.write(shorter_size_url(image))
        
        # Display the uploaded image on the Streamlit app.
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        # Get the file name of the uploaded image.
        file_name = uploaded_image.name.split(".")[0]

        # Create an empty list to store the extracted details for the current image.
        demo = []

        # Read the text from the uploaded image using EasyOCR.
        reader = easyocr.Reader(['en'])
        image_bytes = uploaded_image.read()
         # Add the image bytes to the dictionary with the file name as the key.
        image_bytes_dict[file_name] = image_bytes

        
        # Process the uploaded image.
        image = reader.readtext(image_bytes)

        # Extract the details from the image.
        for result in image:
            demo.append(result[1])

        # Add the extracted details for the current image to the all_details list.
        all_details.append(demo)

        # Check if the all_details list is empty.
    if len(all_details) > 0:
        # Access the all_details[0] list in Streamlit.
        for i in range(len(all_details)):

            for j in range(len(all_details)):
                if all_details[i][j] == "Selva":
                    d1 = {}
                    st.write(all_details[i])
                    # st.write(image_bytes_dict[file_name])
                    # data = []
                    d1["Name"] = all_details[i][0]
                    d1["Designation"] = all_details[i][1]
                    d1["Primary_Number"] = all_details[i][2]
                    d1["Secondary_Number"] = all_details[i][3]
                    r1 = all_details[i][4].replace(" ",".")
                    r2 = r1.replace("I","1")
                    d1["Website"] = r2
                    d1["Email"] = all_details[i][5]
                    all_details[i][-3],all_details[i][-2] = all_details[i][-2],all_details[i][-3]
                    # st.write(res)
                    ad = str(all_details[i][6]+all_details[i][7]).replace(";",",")
                    st.write(ad)
                    d1["Address"] = ad
                    d1["Company"] = all_details[i][8]+" "+all_details[i][9]
                    d1["Image"] = "file:///C:/Users/GANESH/Downloads/1.html"
                    st.write(d1)
                    # data.append(tuple(str(data1.values())))
                    try:
                        pd.read_sql("ALTER TABLE bz_card ADD CONSTRAINT Name UNIQUE (Name);",conn)
                    except:
                        print("duplicated names not allowed")
                    # Prepare the SQL statement.
                    sql = """INSERT INTO bz_card(Name, Company, Designation, Email, Primary_Number, Secondary_Number, Website, Address ,Image)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    # Insert the data into the table.
                    try:
                        cursor.execute(sql, (d1['Name'], d1['Company'], d1['Designation'], d1['Email'], d1['Primary_Number'], d1['Secondary_Number'], d1['Website'], d1['Address'], d1["Image"]))
                    except mysql.connector.IntegrityError:
                        print("Data not inserted because it was a duplicate.")

                    # Commit the changes.
                    conn.commit()

                    que = pd.read_sql("SELECT * FROM bz_card;",conn)
                    st.write(que)

                elif all_details[i][j] == "Amit kumar":
                    st.write(all_details[i])
                    d2 = {}
                    n1 = all_details[i][0]
                    d2["Name"] = n1
                    d = all_details[i][1]
                    d2["Designation"] = d
                    p1 = all_details[i][2]
                    d2["Primary_Number"] = p1
                    d2["Secondary_Number"] = None
                    # data["secondary_number"].append(res[3])
                    r1 = all_details[i][4]

                    web1 = str(r1[:3]).lower()+"."+all_details[i][5]
                    ad1 = all_details[i][6]+" "+" "+all_details[i][11]+" "+all_details[i][7]+" "+all_details[i][9]
                    st.write(ad1)
                    d2["Website"] = web1
                    e1 = all_details[i][3]
                    d2["Email"] = e1
                    # res[-3],res[-2] = res[-2],res[-3]
                    # st.write(res)
                    # ad = str(res[6]+res[7]).replace(";",",")
                    # st.write(ad)
                
                    d2["Address"] = ad1
                    c1 = all_details[i][8]+" "+all_details[i][10]
                    d2["Company"] = c1
                    d2["Image"] = "file:///C:/Users/GANESH/Downloads/2.html"
                    sql = """INSERT INTO bz_card(Name, Company, Designation, Email, Primary_Number, Secondary_Number, Website, Address, Image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    # Insert the data into the table.
                    try:
                        cursor.execute(sql, (d2['Name'], d2['Company'], d2['Designation'], d2['Email'], d2['Primary_Number'], d2['Secondary_Number'], d2['Website'], d2['Address'], d2["Image"]))
                    except mysql.connector.IntegrityError:
                        print("Data not inserted because it was a duplicate.")

                    # Commit the changes.
                    conn.commit()

                    que = pd.read_sql("SELECT * FROM bz_card;",conn)
                    st.write(que)

                if all_details[i][j] == "KARTHICK":
                    d3 = {}
                    st.write(all_details[i])
                    n2 = all_details[i][0]
                    d3["Name"] = n2
                    d2 = all_details[i][1]
                    d3["Designation"] = d2
                    p2 = all_details[i][4]
                    d3["Primary_Number"] = p2
                    d3["Secondary_Number"] = None
                    # data["secondary_number"].append(res[3])
                    web2 = all_details[i][6].replace(" ",".")

                    # st.write(r1)
                    ad2 = all_details[i][2] + " " + all_details[i][3]
                    st.write(ad2)
                    e2 = all_details[i][5]
                    d3["Website"] = web2
                    d3["Email"] = e2
                    # res[-3],res[-2] = res[-2],res[-3]
                    # st.write(res)
                    # ad = str(res[6]+res[7]).replace(";",",")
                    # st.write(ad)
                
                    d3["Address"] = ad2
                    c2 = all_details[i][7]+" "+all_details[i][8]
                    d3["Company"] = c2
                    d3["Image"] = "file:///C:/Users/GANESH/Downloads/3.html"
                    sql = """INSERT INTO bz_card(Name, Company, Designation, Email, Primary_Number, Secondary_Number, Website, Address, Image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    # Insert the data into the table.
                    try:
                        cursor.execute(sql, (d3['Name'], d3['Company'], d3['Designation'], d3['Email'], d3['Primary_Number'], d3['Secondary_Number'], d3['Website'], d3['Address'],d3["Image"]))
                    except mysql.connector.IntegrityError:
                        print("Data not inserted because it was a duplicate.")

                    # Commit the changes.
                    conn.commit()

                    que = pd.read_sql("SELECT * FROM bz_card;",conn)
                    st.write(que)

                if all_details[i][j] == "REVANTH":
                    st.write(all_details[i])
                    d4 = {}
                    n3 = all_details[i][0]
                    d4["Name"] = n3
                    d3 = all_details[i][1]
                    d4["Designation"] = d3
                    p3 = all_details[i][4]
                    d4["Primary_Number"] = p3
                    d4["Secondary_Number"] = None
                    # data["secondary_number"].append(res[3])
                    web3 = all_details[i][7][:3].lower() + "." + all_details[i][7][4:]

                    # st.write(r1)
                    ad3 = all_details[i][2][:11] + " " + all_details[i][2][11:] + " " +all_details[i][3]
                    st.write(ad3)
                    e3 = all_details[i][5]
                    d4["Website"] = web3
                    d4["Email"] = e3
                    # res[-3],res[-2] = res[-2],res[-3]
                    # st.write(res)
                    # ad = str(res[6]+res[7]).replace(";",",")
                    # st.write(ad)
                
                    d4["Address"] = ad3
                    c3 = all_details[i][6] + " " + all_details[i][8]
                    d4["Company"] = c3
                    d4["Image"] = "file:///C:/Users/GANESH/Downloads/4.html"
                    sql = """INSERT INTO bz_card(Name, Company, Designation, Email, Primary_Number, Secondary_Number, Website, Address, Image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    # Insert the data into the table.
                    try:
                        cursor.execute(sql, (d4['Name'], d4['Company'], d4['Designation'], d4['Email'], d4['Primary_Number'], d4['Secondary_Number'], d4['Website'], d4['Address'],d4["Image"]))
                    except mysql.connector.IntegrityError:
                        print("Data not inserted because it was a duplicate.")

                    # Commit the changes.
                    conn.commit()

                    que = pd.read_sql("SELECT * FROM bz_card;",conn)
                    st.write(que)

                if all_details[i][j] == "SANTHOSH":
                    st.write(all_details[i])
                    d5 = {}
                    n4 = all_details[i][0]
                    d5["Name"] = n4
                    d = all_details[i][1]
                    d5["Designation"] = d
                    r1 = all_details[i][2].replace(";",",")
                    ad4 = r1 + " " + all_details[i][3]
                    d5["Address"] = ad4
                    p4 = all_details[i][4]
                    d5["Primary_Number"] = p4
                    d5["Secondary_Number"] = None
                    e4 = all_details[i][5]
                    d5["Email"] = e4
                    web4 = all_details[i][6][:7] + "." + all_details[i][6][-3:]
                    d5["Website"] = web4
                    c4 = all_details[i][7]
                    d5["Company"] = c4
                    d5["Image"] = "file:///C:/Users/GANESH/Downloads/5.html"
                    sql = """INSERT INTO bz_card(Name, Company, Designation, Email, Primary_Number, Secondary_Number, Website, Address, Image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    # Insert the data into the table.
                    try:
                        cursor.execute(sql, (d5['Name'], d5['Company'], d5['Designation'], d5['Email'], d5['Primary_Number'], d5['Secondary_Number'], d5['Website'], d5['Address'],d5["Image"]))
                    except mysql.connector.IntegrityError:
                        print("Data not inserted because it was a duplicate.")

                    # Commit the changes.
                    conn.commit()

                    que = pd.read_sql("SELECT * FROM bz_card;",conn)
                    st.write(que)

        st.warning("""**Note** : after uploading and inserting into Mysql table refresh dashboard once to get faster response of updation and deletion 
            Why beacause of Streamlit needs to render the UI and update the state whenever data is inserted or updated.""")

    else:
        # The all_details list is empty.
        st.write("No images have been uploaded yet.")

    





def update():
    container = st.container()
    try:
        with container:
            @st.cache_data(ttl=60 * 60)
            def load_lottie_file(filepath : str):
                with open(filepath, "r") as f:
                    gif = json.load(f)
                st_lottie(gif, speed=1, width=800, height=450)
                
            load_lottie_file("update.json")
    except:
        print("Don't raise exception")

    st.header("update the database contents")
    cursor.execute("select name from bz_card")
    get = cursor.fetchall()
    name = []
    for i in get:
        name.extend(list(i))
    # st.write(name)
    # Create a select box
    opt = st.selectbox('choose name to update:', name,key = "opt")
    # If the selected name is "Selva", show a text input to enter the new name
    cursor.execute(f"select * from bz_card where name = '{opt}'")
    get = cursor.fetchall()
    data = []
    for i in get:
        data.extend(list(i))
    # st.write(data)
    new_name = st.text_input("Enter the new name:",data[0])
    if new_name:
        def up_name():
            # Update the name in the MySQL database
            cursor.execute(f"UPDATE bz_card SET name = '{new_name}' WHERE name = '{opt}'")

            # Commit the changes
            conn.commit()
            # Close the cursor object and the connection to the database
            cursor.close()
            conn.close()
            

        # Create a button to update the name
        but1 = st.button("Update Name",on_click=up_name)
        if but1:
            st.subheader("Name Successfully updated")
        
    new_company = st.text_input("Enter the new company:",data[1])
    if new_company:
        def up_com():
            # Update the name in the MySQL database
            cursor.execute(f"UPDATE bz_card SET Company = '{new_company}' WHERE name = '{opt}'")

            # Commit the changes
            conn.commit()
            # Close the cursor object and the connection to the database
            cursor.close()
            conn.close()
            
        # Create a button to update the name
        but2 = st.button("Update Company",on_click=up_com)
        if but2:
            st.subheader("company name Successfully updated")
            
    
    new_designation = st.text_input("Enter the new designation:",data[2])
    if new_designation:
        def up_des():
            # Update the name in the MySQL database
            cursor.execute(f"UPDATE bz_card SET Designation = '{new_designation}' WHERE name = '{opt}'")

            # Commit the changes
            conn.commit()
            # Close the cursor object and the connection to the database
            cursor.close()
            conn.close()
            
        # Create a button to update the name
        but3 = st.button("Update Designation",on_click=up_des)
        if but3:
            st.subheader("Designation Successfully updated")
        
            
    

    new_email = st.text_input("Enter the new Email:",data[3])

    if new_email:
        def up_email():
            # Update the name in the MySQL database
            cursor.execute(f"UPDATE bz_card SET Email = '{new_email}' WHERE name = '{opt}'")

            # Commit the changes
            conn.commit()
            # Close the cursor object and the connection to the database
            cursor.close()
            conn.close()
            
        # Create a button to update the name
        but4 = st.button("Update Email address",on_click=up_email)
        if but4:
            st.subheader("Email address Successfully updated")
            
    

    new_pri = st.text_input("Enter the new Primary_number:",data[4])
    if new_pri:
        def up_pri():
            # Update the name in the MySQL database
            cursor.execute(f"UPDATE bz_card SET Primary_Number = '{new_pri}' WHERE name = '{opt}'")

            # Commit the changes
            conn.commit()
            # Close the cursor object and the connection to the database
            cursor.close()
            conn.close()
            
        # Create a button to update the name
        but5 = st.button("Update Primary_Number",on_click=up_pri)
        if but5:
            st.subheader("Primary Number Successfully updated")
            
        

    new_sec = st.text_input("Enter the new Secondary_number:",data[5])
    def up_sec():
        # Update the name in the MySQL database
        cursor.execute(f"UPDATE bz_card SET Secondary_Number = '{new_sec}' WHERE name = '{opt}'")

        # Commit the changes
        conn.commit()
        # Close the cursor object and the connection to the database
        cursor.close()
        conn.close()
        
    # Create a button to update the name
    but6 = st.button("Update Secondary_Number",on_click=up_sec)
    if but6:
        st.subheader("Secondary Number Successfully updated")
        

    new_web = st.text_input("Enter the new Webiste URL:",data[6])
    def up_web():
        # Update the name in the MySQL database
        cursor.execute(f"UPDATE bz_card SET Website = '{new_web}' WHERE name = '{opt}'")

        # Commit the changes
        conn.commit()
        # Close the cursor object and the connection to the database
        cursor.close()
        conn.close()
        
    # Create a button to update the name
    but7 = st.button("Update Website URL",on_click=up_web)
    if but7:
       st.subheader("Websie URL Successfully updated")
            
        
            
    new_add = st.text_input("Enter the new Address:",data[7])
    def up_add():
        # Update the name in the MySQL database
        cursor.execute(f"UPDATE bz_card SET Address = '{new_add}' WHERE name = '{opt}'")

        # Commit the changes
        conn.commit()
        # Close the cursor object and the connection to the database
        cursor.close()
        conn.close()
        
    # Create a button to update the name
    but8 = st.button("Update Address",on_click=up_add)
    if but8:
        st.subheader("Address Successfully updated")
            

# Create a button to upload the file







def delete():
    container = st.container()
    try:
        with container:
            @st.cache_data(ttl=60 * 60)
            def load_lottie_file(filepath : str):
                with open(filepath, "r") as f:
                    gif = json.load(f)
                st_lottie(gif, speed=1, width=800, height=450)
                
            load_lottie_file("delete.json")
    except:
        print("Don't raise exception")

    st.header("delete the database contents")

    cursor.execute("select name from bz_card")
    get = cursor.fetchall()
    name = []
    for i in get:
        name.extend(list(i))
    
    opt1 = st.selectbox('choose name to delete:', name,key="opt1")
   
    # Define a function to delete the name
    def del_name():
        # Delete the name from the database
        cursor.execute(f"DELETE FROM bz_card WHERE name = '{opt1}';")

        # Commit the changes
        conn.commit()
    
    # Create a button to delete the name
    but = st.button("Delete Name",on_click=del_name,key="delete_name")

    # Check if the button is clicked
    if but:
        st.subheader("Name of the row deleted successfully from table")



# Create a button to upload the file



menu_options = ["Upload", "Update", "Delete"]

# Create the menu bar
with st.sidebar:
    selected = option_menu("Main Menu", menu_options)

# Display the selected page
page_functions = {
    "Upload": upload,
    "Update": update,
    "Delete": delete
}
page_functions[selected]()

