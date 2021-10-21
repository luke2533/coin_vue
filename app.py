import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from coinvue import Crypto
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

crypto = Crypto()

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")


@app.route("/coinvue")
def coinvue():
    results = crypto.get_top_50()

    for result in results:
        result["quote"]["USD"]["price"] = "$ " + "{:.4f}".format(result["quote"]["USD"]["price"])
    # The {:.4f} is the number of decimal places
    return render_template("index.html", **locals())


@app.route("/portfolio")
def portfolio():
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    
    if session["user"]:
        return render_template("portfolio.html", username=username)



# Function for users to sign up
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
    
        if existing_user:
            flash("Username already exisits")
            return redirect(url_for("signup"))
    
        password = request.form.get("password")
        check_password = request.form.get("confirm-password")
        email = request.form.get("email")
        check_email = request.form.get("confirm-email")

        if password != check_password:
            flash("Please make sure the passwords match")
            return redirect(url_for("signup"))

        if email != check_email:
            flash("Please make sure the emails match")
            return redirect(url_for("signup"))

        new_user = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(new_user)

        session["user"] = request.form.get("username").lower()
        flash("Register complete")
    return render_template("signup.html")


# Function for users to log in
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #Checks database for username
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username")
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(url_for("profile", username=session["user"]))
            else:
                #Wrong password
                flash("Inccorect Username and/or Password")
                return redirect(url_for("login"))

        else:
            #Username does't exist
            flash("Inccorect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Function for signed in users
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    #Grabs session users username
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    
    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


# Function for users to sign out
@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect((url_for("login")))


# @app.route("/portfolio")
# def portfolio():
#     return render_template("portfolio.html")

# CRUD

# CREATE
@app.route("/add_record", methods=["GET", "POST"])
def add_record():
    if request.method == "POST":
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

        quantity = request.form.get("quantity")
        per_coin = request.form.get("per-coin")
        total = float(quantity) * float(per_coin)

        record = {
            "username": session["user"],
            "name": request.form.get("name"),
            "quantity": request.form.get("quantity"),
            "per-coin": request.form.get("per-coin"),
            "date": request.form.get("date"),
            "notes": request.form.get("notes"),
            "total": total
        }
        mongo.db.cryptos.insert_one(record)
        flash("Crypto Successfuly Added")
        return redirect(url_for("portfolio"))

    return render_template("portfolio.html", username=username)


# READ
# @app.route("/get_record")
# def get_record():
#     username = mongo.db.cryptos.find_one(
#         {"username": session["user"]})["username"]

#     #This is where you add the variables for each equation

# # name grabs to coins name from the cryptos collection underneath the same username
#     name = mongo.db.cryptos.find(
#         {"name": "Bitcoin"})
#         # To test will just use bitcoin for now
        
# # e


#     portfolio = {
#         "username": session["user"],
#         "name": name,
#         "price": price,
#         "price_change": price_change,
#         "holdings": holdings,
#         "value": value,
#         "grand_total": grand_total,
#         "profit_loss": profit_loss
#     }
#     # This doesn't work "key": "value" using mongo.db.find just finds nothing 
#     # because nothing is there at the moment
#     mongo.db.portfolios.insert_one(portfolio)

# # Need to figure out how to build record for portfolio and how to access and change it

#     return render_template(("portfolio.html"), username=username)
    


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)
