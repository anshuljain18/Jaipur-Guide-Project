from flask import Flask, request, redirect, url_for, render_template
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import sqlite3, os, json

with open("config.json", "r") as f:
    params = json.load(f)["params"]

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder="templates")

app.config['UPLOAD_FOLDER'] = params['upload_folder']
app.static_folder = "./static"
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = params['email_id']
app.config['MAIL_PASSWORD'] = params['email_passwd']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_email(subject, sender, recipient, msg):
    print("-->"*20,subject, sender, recipient, msg)
    mail.send_message(
        subject,
        sender=sender,
        recipients=[recipient],
        body=msg
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/facts")
def facts():
    return render_template("facts.html")

@app.route("/tourist_place")
def tourist_place():
    with sqlite3.connect("Travel.db") as con:
      cur = con.cursor()
      info = cur.execute("SELECT * FROM Jaipur;")
      con.commit()
    information = [dict(name=row[1], image=row[2], desc=row[4]) for row in info]
    return render_template("tourist_place.html", information=information, heading="Tourist Places")

@app.route("/category/<category>")
def categorize(category):
    with sqlite3.connect("Travel.db") as con:
      cur = con.cursor()
      info = cur.execute(f"SELECT * FROM Jaipur WHERE tag = '{category}';")
      con.commit()
    information = [dict(name=row[1], image=row[2], desc=row[4]) for row in info]
    more_btn = 1
    if category == "gardens":
        heading = "Parks / Gardens"
    elif category == "wildlife":
        heading = "Nature / Wildlife"
    elif category == "food":
        heading = "Food Delicacies"
    else:
        heading = category

    if category in  ["shopping", "food", "festivals"]:
        more_btn = 0

    return render_template("tourist_place.html", information=information, heading=heading, more_btn=more_btn)

@app.route("/place/<name>")
def detail(name):
    ## ---------------------- Working -----------------
    print("--"*30,name,"--"*30)
    # with sqlite3.connect("Travel.db") as con:
    #   cur = con.cursor()
    #   info = cur.execute(f"SELECT * FROM Jaipur WHERE tag = '{name}';")
    #   con.commit()
    return render_template("more_info.html", name=name)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        place_name = request.form.get("place_name")
        address = request.form.get("address")
        tag = request.form.get("category")
        desc = request.form.get("description")
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = place_name + ".jpg"
            
            if email == params["email_id"]:
                file.save(os.path.join(params['image_folder'], filename))
                with sqlite3.connect("Travel.db") as con:
                    image = "img/" + filename
                    cur = con.cursor()
                    cur.execute(f'INSERT INTO Jaipur ("name", "image", "tag", "desc") VALUES(?,?,?,?);',(place_name, image, tag, desc))
                    con.commit()
                print("--"*20, "Data is saved by Admin!!")
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print("--"*20, "Data is saved!!")

        else:
            return render_template("add.html")
        return redirect("/")
    else:
        return render_template("add.html")

@app.route("/contact", methods=['GET','POST'])
def contact():
    if request.method == "POST":
        user_name = request.form.get("username")
        email = request.form.get("email")
        phone_no = request.form.get("phone_number")
        suggestion = request.form.get("suggestion")
        print("-"*10, user_name, email, phone_no, suggestion)

        with sqlite3.connect("Travel.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Suggestion (username, email, contact, suggestion) VALUES (?,?,?,?);",(user_name,email,phone_no,suggestion))
            con.commit()

        subject = 'Thank you for reponse'
        user_msg = f"Dear {user_name},\n\nWe are glad to have your response. Hope you loved our website and gained information.\n\n\n\nRegards,\nJaipur Guide Team"
        admin_sbj = f"Suggestion from {user_name}"
        admin_msg = f"{suggestion} \n\n{user_name}\n{phone_no}"
        send_email(subject, params['email_id'], email, user_msg)
        send_email(admin_sbj, email, params['email_id'], admin_msg)

        return render_template("contact.html")
    else:
        return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)