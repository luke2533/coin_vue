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

    record = mongo.db.cryptos.find_one({"_id": ObjectId()})

    if session["user"] == username:
        user_record = mongo.db.cryptos.find({"username": session["user"]}).sort("date", -1)
    
    for price in prices:
        price["quote"]["USD"]["price"] = "$" + "{:.4f}".format(price["quote"]["USD"]["price"])
        price["quote"]["USD"]["percent_change_24h"] = "{}%".format(price["quote"]["USD"]["percent_change_24h"])

    if session["user"]:
        return render_template("portfolio.html", username=username, names=names, prices=prices, record=record, user_record=user_record)



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
                    # return redirect(url_for("profile", username=session["user"]))
                    return redirect(url_for("portfolio"))
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

        type = request.form.get("type")
        quantity = request.form.get("quantity")
        per_coin = request.form.get("per_coin")
        total = float(quantity) * float(per_coin)
        # price = 2
        # PLACEHOLDER VALUE
        # value = float(price) * float(holdings)
        # profit_loss = float(value) - float(total)
        coin_id = request.form.get("coin_id")
        # coin_id_exists = False
        # coin_id_object = {}
        # get_coins = mongo.db.portfolios.find(
        #     {"username": session["user"]}
        # )
        # Finds all of the portfolios and matches the username to the user

        # for get_coin in get_coins:
        #     for token in get_coin.get("id"):
        #         # Loops through the array for the "token" that matches the coin_id
        #         if token.get("coin_id") == coin_id:
        #             coin_id_exists = True
        #             coin_id_object = token
                    # If there is a match my_portfolios fills crypto_id_object with the data

        records = {
            "username": session["user"],
            "type": type,
            "coin_id": coin_id,
            "quantity": float(quantity),
            "per_coin": float(per_coin),
            "date": request.form.get("date"),
            "notes": request.form.get("notes"),
            "total": float(total)
        }
        mongo.db.cryptos.insert_one(records)

        # find_portfolio = mongo.db.portfolios.find_one(
        #     {"username": session["user"]})["username"]
            # Finds username that matches the current users account

        # if find_portfolio == username and coin_id_exists == True:

        #     updated_holdings = float(quantity) + float(coin_id_object.get("holdings"))
        #     updated_value = float(price) * float(coin_id_object.get("holdings"))
        #     # Might need help with this bit
        #     updated_total = float(total) + float(coin_id_object.get("grand_total"))
        #     updated_profit = float(coin_id_object.get("value")) - float(coin_id_object.get("grand_total"))
            
        #     # delete by old portfolio and append the new information into the array then insert the entire new object
        #     if type == "Buy" or type == "Staking":
        #         my_portfolios = {
        #             "username": session["user"],
        #             "id": [{
        #                 "coin_id": coin_id,
        #                 "holdings": updated_holdings,
        #                 "value": updated_value,
        #                 "grand_total": updated_total,
        #                 "profit_loss": updated_profit
        #             }]
        #         }
        #         mongo.db.portfolios.update_one(my_portfolios)
                
        #     elif type == "Sell":
        #         sell_holdings = float(coin_id_object.get("holdings")) - float(quantity)
        #         sell_total = float(coin_id_object.get("grand_total")) - float(coin_id_object.get("value"))

        #         my_portfolios = {
        #             "username": session["user"],
        #             "id": [{
        #                 "coin_id": coin_id,
        #                 "holdings": sell_holdings,
        #                 "value": updated_value,
        #                 "grand_total": sell_total,
        #                 "profit_loss": updated_profit
        #             }]
        #         }
        #         mongo.db.portfolios.update_one(my_portfolios)
        #     # If the username and coin_id match a record in the portfolios collection it adds the users new data

        # elif find_portfolio == username and coin_id_exists == False:
        #     my_portfolios = {
        #         "username": session["user"],
        #         "id": [{
        #             "coin_id": coin_id,
        #             "holdings": quantity,
        #             "value": value,
        #             "grand_total": total,
        #             "profit_loss": profit_loss
        #         }]
        #     }
        #     mongo.db.portfolios.update_many(my_portfolios)
        #     # NEED TO FIGURE OUT HOW TO ADD A NEW ID IN THE ARRAY
        #     # If the username matches but coin_id does not then it creates a new array within ID

        # else:
        #     my_portfolios = {
        #         "username": session["user"],
        #         "id": [{
        #             "coin_id": coin_id,
        #             "holdings": quantity,
        #             "value": value,
        #             "grand_total": total,
        #             "profit_loss": profit_loss
        #         }]
        #     }
        #     mongo.db.portfolios.insert_one(my_portfolios)
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


# Edit
@app.route("/edit_record/<record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    if request.method == "POST":

        coin_id_example = "Bitcoin"
        quantity_edit = request.form.get("quantity_edit")
        per_coin_edit = request.form.get("per_coin_edit")
        total_edit = float(quantity_edit) + float(per_coin_edit)

        update_record = {
            "username": session["user"],
            "type": type,
            "coin_id": coin_id_example,
            "quantity": float(quantity_edit),
            "per_coin": float(per_coin_edit),
            "date": request.form.get("date_edit"),
            "notes": request.form.get("notes_edit"),
            "total": float(total_edit)
        }
        mongo.db.cryptos.update({"_id": ObjectId(record_id)}, update_record)
        flash("Record Succesfully Updated")
    
    record = mongo.db.cryptos.find_one({"_id": ObjectId(record_id)})
    return render_template("portfolio.html", record=record)
    # Code institute task manager edit


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)
