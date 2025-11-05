# Importing essential libraries and modules

from flask import Flask, render_template, request, Markup
import numpy as np
#import pandas as pd
import os
import requests
import config
import pickle
import io
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ==============================================================================================
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
# -------------------------LOADING THE TRAINED MODELS -----------------------------------------------

gmail_list=[]
password_list=[]
gmail_list1=[]
password_list1=[]



#disease_dic= ["Eye Spot","Healthy Leaf","Red Leaf Spot","Redrot","Ring Spot"]



from model_predict2  import pred_skin_disease

# ===============================================================================================
# ------------------------------------ FLASK APP -------------------------------------------------


app = Flask(__name__)

# render home page

@app.route('/')
def home():
    return render_template('login44.html')  


@app.route('/register22',methods=['POST','GET'])
def register22():
    return render_template('register44.html')  

@app.route('/logedin',methods=['POST'])
def logedin():
    
    int_features3 = [str(x) for x in request.form.values()]
    print(int_features3)
    logu=int_features3[0]
    passw=int_features3[1]
   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root","","ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              #print(result1)
              #print(gmail1)
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list.append(str(row1[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(gmail_list)
    

    cursor1= db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2=cursor1.fetchall()
              #print(result1)
              #print(gmail1)
    for row2 in result2:
                      print(row2)
                      print(row2[0])
                      password_list.append(str(row2[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(password_list)
    print(gmail_list.index(logu))
    print(password_list.index(passw))
    
    if gmail_list.index(logu)==password_list.index(passw):
        return render_template('index.html')
    else:
        return jsonify({'result':'use proper  gmail and password'})
                  
                                               



                          
                     # print(value1[0:])
    
    
    
    

              
              # int_features3[0]==12345 and int_features3[1]==12345:
               #                      return render_template('index.html')
        
@app.route('/register',methods=['POST'])
def register():
    

    int_features2 = [str(x) for x in request.form.values()]
    #print(int_features2)
    #print(int_features2[0])
    #print(int_features2[1])
    r1=int_features2[0]
    print(r1)
    
    r2=int_features2[1]
    print(r2)
    logu1=int_features2[0]
    passw1=int_features2[1]
        
    

    

   # if int_features2[0]==12345 and int_features2[1]==12345:

    import MySQLdb


# Open database connection
    db = MySQLdb.connect("localhost","root",'',"ddbb" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              #print(result1)
              #print(gmail1)
    for row1 in result1:
                      print(row1)
                      print(row1[0])
                      gmail_list1.append(str(row1[0]))
                      
                      #gmail_list.append(row1[0])
                      #value1=row1
                      
    print(gmail_list1)
    if logu1 in gmail_list1:
                      return jsonify({'result':'this gmail is already in use '})  
    else:

                  #return jsonify({'result':'this  gmail is not registered'})
              

# Prepare SQL query to INSERT a record into the database.
                  sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
                  val = (r1, r2)
   
                  try:
   # Execute the SQL command
                                       cursor.execute(sql,val)
   # Commit your changes in the database
                                       db.commit()
                  except:
   # Rollback in case there is any error
                                       db.rollback()

# disconnect from server
                  db.close()
                 # return jsonify({'result':'succesfully registered'})
                  return render_template('login44.html')

                      






#@ app.route('/')
#def home():
#    title = 'Vitamin Deficiency Prediction Based on Skin Disease'
#    return render_template('index.html', title=title)

# render crop recommendation form page

@app.route('/disease-predict', methods=['GET', 'POST'])
def disease_prediction():
    title = 'Vitamin Deficiency Prediction Based on Skin Disease'

    if request.method == 'POST':
        file = request.files.get('file')

        if not file:
            return render_template('rust.html', title=title)

        # Process the uploaded file
        img = Image.open(file)
        img.save('output.png')

        # Make the prediction
        prediction,accuracy = pred_skin_disease("output.png")
        #prediction = str(disease_dic[prediction])

        print("Prediction result:", prediction)
    # Define details for each disease
        # Define details for each sugarcane disease


        ## Define the class names
        #class_names = ["Bacterial Pneumonia", "Corona Virus Disease", "Normal", "Tuberculosis","Viral Pneumonia"]

# Disease information for Diabetic Retinopathy
        disease_info = {
            "Mild": {
                "cause": "Early-stage diabetic retinopathy with microaneurysms.",
                "treatment": "Control blood sugar levels; regular monitoring and lifestyle changes."
            },
            "Moderate": {
                "cause": "Progressing diabetic retinopathy with increased damage to retinal blood vessels.",
                "treatment": "Control blood sugar and blood pressure; consider laser treatment if necessary."
            },
            "No_DR": {
                "cause": "No signs of diabetic retinopathy detected.",
                "treatment": "Maintain healthy blood sugar levels and routine eye check-ups."
            },
            "Proliferate_DR": {
                "cause": "Advanced stage with abnormal blood vessel growth in the retina.",
                "treatment": "Immediate medical attention; treatments include laser therapy, anti-VEGF injections, or surgery."
            },
            "Severe": {
                "cause": "Severe non-proliferative diabetic retinopathy with extensive blood vessel blockage.",
                "treatment": "Urgent care; may require laser treatment or anti-VEGF injections."
            }
        }

        # Fetch the disease details
        details = disease_info.get(prediction, {})
        cause = details.get("cause", "Unknown condition detected.")
        treatment = details.get("treatment", "No treatment information available.")

        # Render the result page with the prediction and details
        return render_template(
            'rust-result.html', 
            prediction=prediction, 
            cause=cause, 
            treatment=treatment, 
            title="Disease Information",
            accuracy=accuracy
        )

    # Default page rendering
    return render_template('rust.html', title=title)



from flask import make_response,send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    prediction = request.form.get('prediction')
    cause = request.form.get('cause')
    treatment = request.form.get('treatment')

    # Create PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add content
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 100, "Diabetic Retinopathy Detection Report")

    p.setFont("Helvetica", 12)
    p.drawString(100, height - 140, f"Disease Prediction: {prediction}")
    p.drawString(100, height - 160, f"Cause: {cause}")
    p.drawString(100, height - 180, f"Treatment: {treatment}")

    p.save()

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="Diabetic_Retinopathy_Report.pdf",
        mimetype='application/pdf'
    )

# render disease prediction result page


# ===============================================================================================
if __name__ == '__main__':
    app.run(debug=True)
