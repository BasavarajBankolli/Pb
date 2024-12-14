from flask import *
from pymongo import  *
import json
import subprocess

clinet = MongoClient("mongodb://localhost:27017/")

db = clinet["smart_att"]
col1 = db["verification"]

app = Flask (__name__)
app.secret_key = "pb"

@app.route("/")
@app.route("/login")
def login():

    return render_template("login.html")

@app.route("/login_verification",methods=["POST"])
def login_verification():
    data = request.form
    mail = data["email"]

    x = col1.find_one({"mail": mail},{"_id":0})

    if x:

        password = data["password"]

        if password == x["password"]:
            return redirect(url_for("home"))

        else:
            flash("Incorrect mailID or password")




    else:

        flash("user not exists")

    return render_template("login.html")





@app.route("/sign_up")
def sign_up():


    return render_template("signup.html")

@app.route("/signup_verification",methods=["POST"])
def signup_verification():

    data = request.form
    mail = data["email"]

    x = col1.find_one({"mail": mail})

    if not (x):

        password = data["password"]
        conpass = data["confirm_password"]

        if password == conpass:

            col1.insert_one({"mail": mail, "password": password})

            return render_template("login.html")


        else:
            flash("password miss match")
            return render_template("signup.html")

    flash("Your account is already exists")

    return render_template("signup.html")

@app.route("/home")
def home():

    with open(r"C:\Users\pvb02\Desktop\mini pro\smart\pairs.json",'r') as file:

           data1 = json.load(file)

    with open(r"C:\Users\pvb02\Desktop\mini pro\smart\attendance.json",'r') as f:

            ids = json.load(f)




    return render_template("home.html",data = data1, ids=ids,sort = sorted)

@app.route("/run_datacollect")
def run_datacollect():
    try:
        # Run the datacollect script
        subprocess.Popen(["python", r"C:\Users\pvb02\Desktop\mini pro\smart\dataCollect.py"])
        return {"success": True}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False}


@app.route("/run_training")
def run_training():
    try:
        subprocess.run(["python", r"C:\Users\pvb02\Desktop\mini pro\smart\classifireTrainig.py"], check=True)
        return {"success": True}
    except subprocess.CalledProcessError as e:
        print(f"Training failed: {e}")
        return {"success": False}


app.run(debug=True)