from flask import Flask, render_template, send_from_directory, request
import os, time, csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<filename>")
def pages(filename=None):
    try:
        print(filename)
        return render_template(filename)
    except:
        return "This page was not found. Redirecting"
    
def store_data_txt(data):
    email = data["email"]
    subject = data["subject"]
    message = data["message"]
    with open("database.txt", mode="a", encoding=("utf-8")) as database:
        database.write(f"\n{email} : {subject} : {message}")
    
def store_data_csv(data):
    email = data["email"]
    subject = data["subject"]
    message = data["message"]
    with open("database.csv", mode="a", encoding=("utf-8"), newline="") as database2:
        csv_writer = csv.writer(database2, dialect="excel", delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form(msg=None):
    if request.method == "POST":
        
        data = request.form.to_dict()
        def missing_data():
            form_var = False
            if data["email"] == "" :
                    form_var = "Email"

            elif data["subject"] == "":
                form_var = "Subject"

            elif data["message"] == "":
                    form_var = "Message"
            return form_var
                
        if missing_data():
            return render_template("contact.html", msg=f"{missing_data()} is requied!")
        else:
            try:
                store_data_csv(data)
                return render_template("contact.html", msg="We will be in touch with you!")
            except:
                return render_template("contact.html", msg="We couldnt store data, sorry")
