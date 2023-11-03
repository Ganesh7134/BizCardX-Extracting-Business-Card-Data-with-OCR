# BizCardX-Extracting-Business-Card-Data-with-OCR
**Overview**

BizCardX is a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information includes the company name, card holder name, designation, mobile number, email address, website URL, area, city, state, and pin code. The extracted information is then displayed in the application's GUI. Additionally, the application allows users to save the extracted information into a database along with the uploaded business card image. The database can store multiple entries, each with its own business card image and extracted information.

**Features**

* Upload a business card image and extract relevant information using easyOCR.
* Display the extracted information in a clean and organized manner.
* Save the extracted information into a database along with the uploaded business card image.
* Read, update, and delete data in the database through the Streamlit UI.

**System Requirements**

* Python 3.6 or higher
* Streamlit
* easyOCR
* A database management system like SQLite or MySQL

**Installation**

> pip install -r requirements.txt

**Usage**

1.Run the Streamlit app: streamlit run app.py

2.Upload an image of a business card and click the "Extract" button.

3.Review the extracted information and click the "Save" button to save it to the database.

4.To view, update, or delete data in the database, click the "Manage Data" button.

**Conclusion**

BizCardX is a powerful tool that can help users to quickly and easily extract relevant information from business cards. The application is easy to use and has a simple and intuitive user interface. The extracted information can be saved to a database for future reference, and users can also read, update, and delete data in the database through the Streamlit UI. BizCardX is a valuable tool for anyone who needs to manage large volumes of business card data.
