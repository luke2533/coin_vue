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
        result["quote"]["USD"]["price"] = "$" + "{:.4f}".format(result["quote"]["USD"]["price"])
        result["quote"]["USD"]["market_cap"] = "$" + "{:.2f}".format(result["quote"]["USD"]["market_cap"])
        result["quote"]["USD"]["volume_24h"] = "$" + "{:.2f}".format(result["quote"]["USD"]["volume_24h"])
        result["quote"]["USD"]["percent_change_24h"] = "{:.4f}%".format(result["quote"]["USD"]["percent_change_24h"])
    # The {:.4f} is the number of decimal places
    return render_template("index.html", **locals())


@app.route("/portfolio")
def portfolio():
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    names = crypto.get_name()

    prices = crypto.get_price()

    for price in prices:
        price["quote"]["USD"]["price"] = "$" + "{:.4f}".format(price["quote"]["USD"]["price"])
        price["quote"]["USD"]["percent_change_24h"] = "{}%".format(price["quote"]["USD"]["percent_change_24h"])

    if session["user"]:
        return render_template("portfolio.html", username=username, names=names, prices=prices)



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
                # Wrong password
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


# CRUD

# CREATE
@app.route("/add_record", methods=["GET", "POST"])
def add_record():

    if request.method == "POST":
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

        # Collects the data from the users form

        quantity = request.form.get("quantity")
        per_coin = request.form.get("per-coin")
        total = float(quantity) * float(per_coin)
        price = 2
        # PLACEHOLDER VALUE
        value = float(price) * float(quantity)
        profit_loss = float(value) - float(total)
        coin_id = request.form.get("coin_id")
        coin_id_exists = False
        coin_id_object = {}
        get_coins = mongo.db.portfolios.find(
            {"username": session["user"]}
        )
        # Finds all of the portfolios and matches the username to the user

        for get_coin in get_coins:
            for token in get_coin.get("id"):
                # Loops through the array for the "token" that matches the coin_id
                if token.get("coin_id") == coin_id:
                    coin_id_exists = True
                    coin_id_object = token
                    # If there is a match my_portfolios fills crypto_id_object with the data

        

        # crypto_holdings = mongo.db.portfolios.find_one({"id": {"holdings": 1}})
        # print(crypto_holdings)
        # holdings = float(quantity) + float(crypto_holdings)
        # # Finds the current holdings and adds the lastest quantity data to it

        # # price = IDK HOW TO DO THIS YET
        # value = float(holdings) * float(price)
        # # Price finds the current price for the coin_id and value multiplys it with the users holdings

        # crypto_total = mongo.db.portfolios.find_one({"id": {"grand_total": 1}})
        # print(crypto_total)
        # grand_total = float(total) + float(crypto_total)
        # # Finds the current total and adds the latest total data to it

        # profit_loss = float(value) - float(grand_total)
        # If the value is more than the grand_total it will return a postive number otherwise it will return negative (loss)

        records = {
            "username": session["user"],
            "coin_id": coin_id,
            "quantity": float(quantity),
            "per-coin": float(per_coin),
            "date": request.form.get("date"),
            "notes": request.form.get("notes"),
            "total": float(total)
        }
        mongo.db.cryptos.insert_one(records)

        find_portfolio = mongo.db.portfolios.find_one(
            {"username": session["user"]})["username"]
            # Finds username that matches the current users account

        if find_portfolio == username and coin_id_exists == True:

            updated_holdings = float(quantity) + float(coin_id_object.get("holdings"))
            updated_value = float(price) * float(coin_id_object.get("holdings"))
            # Might need help with this bit
            updated_total = float(total) + float(coin_id_object.get("grand_total"))
            updated_profit = float(coin_id_object.get("value")) - float(coin_id_object.get("grand_total"))
            
            # delete by old portfolio and append the new information into the array then insert the entire new object
            my_portfolios = {
                "username": session["user"],
                "id": [{
                    "coin_id": coin_id,
                    "holdings": updated_holdings,
                    "value": updated_value,
                    "grand_total": updated_total,
                    "profit_loss": updated_profit
                }]
            }
            mongo.db.portfolios.update_many(my_portfolios)
            # If the username and coin_id match a record in the portfolios collection it adds the users new data

        elif find_portfolio == username and coin_id_exists == False:
            my_portfolios = {
                "username": session["user"],
                "id": [{
                    "coin_id": coin_id,
                    "holdings": quantity,
                    "value": value,
                    "grand_total": total,
                    "profit_loss": profit_loss
                }]
            }
            mongo.db.portfolios.update_many(my_portfolios)
            # NEED TO FIGURE OUT HOW TO ADD A NEW ID IN THE ARRAY
            # If the username matches but coin_id does not then it creates a new array within ID

        else:
            my_portfolios = {
                "username": session["user"],
                "id": [{
                    "coin_id": coin_id,
                    "holdings": quantity,
                    "value": value,
                    "grand_total": total,
                    "profit_loss": profit_loss
                }]
            }
            mongo.db.portfolios.insert_one(my_portfolios)
            # If the username and coin_id does not then it creates a new record / new portfolio

        flash("Crypto Successfuly Added")
        return redirect(url_for("portfolio"))

    return render_template("portfolio.html",
        username=username, **locals())


# READ
@app.route("/get_record")
def get_record():
    username = mongo.db.cryptos.find_one(
        {"username": session["user"]})["username"]

    return render_template(("portfolio.html"), username=username)
    


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)
