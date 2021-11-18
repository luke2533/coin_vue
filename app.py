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
    # Crypto names used in transaction forms

    prices = crypto.get_price()
    # Displays the prices of users portfolio coins

    record = mongo.db.cryptos.find_one({"_id": ObjectId()})
    # Finds the record id

    delete = mongo.db.cryptos.delete_one({"_id": ObjectId()})
    # Deletes records from users portfolio

    if session["user"] == username:
        user_record = mongo.db.cryptos.find({"username": session["user"]}).sort("date", -1)
    # Displays the users record history

    portfolios = []

    if session["user"] == username:
        user_portfolio_display = mongo.db.portfolios.find_one({"username": session["user"]})
        if user_portfolio_display is not None:
            _id = user_portfolio_display["_id"]
            portfolios = user_portfolio_display["id"]
        # ANOTHER PROBLEM IF USER DOESN'T HAVE ACCOUNT IT DOESN'T WORK
    # Displays the users portfolio
    
    # if session["user"] == username:
    #     user_portfolio_total = mongo.db.portfolios.find_one({"username": session["user"]})
    #     for get_total in user_portfolio_total:
    #         get_id = get_total.get("id")

    #         for total in get_id:
    #             coin_value = float(total.get("value"))
    #             coin_profit = float(total.get("profit_loss"))

    #             total_value = coin_value + coin_value
    #             total_profit = coin_profit + coin_profit
    # Displays the users portfolios total value and its profit or loss

    
    for price in prices:
        price["quote"]["USD"]["price"] = "$" + "{:.4f}".format(price["quote"]["USD"]["price"])
        price["quote"]["USD"]["percent_change_24h"] = "{}%".format(price["quote"]["USD"]["percent_change_24h"])
        # price = price["quote"]["USD"]["price"]
        # price_change = price["quote"]["USD"]["percent_change_24h"]

    if session["user"]:
        return render_template("portfolio.html", username=username, 
            names=names, prices=prices, record=record, user_record=user_record, delete=delete, portfolios=portfolios)
            #total_value=total_value, total_profit=total_profit, delete_all=delete_all, portfolios=portfolios



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
        return redirect(url_for("portfolio"))
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
        price = 2
        # PLACEHOLDER VALUE
        value = float(price) * float(quantity)
        # value = float(price) * float(holdings) is wrong
        profit_loss = float(value) - float(total)
        coin_id = request.form.get("coin_id")
        coin_id_exists = False
        coin_id_object = {}
        coin_id_object_position = 0
        # Finds username that matches the current users account
        user_portfolio_contents = mongo.db.portfolios.find_one(
            {"username": session["user"]}
        )
        print(user_portfolio_contents)
        # Finds all of the portfolios and matches the username to the user

        if user_portfolio_contents is not None:
            for position, token in enumerate(user_portfolio_contents.get("id")):
                # Loops through the array for the "token" that matches the coin_id
                if token.get("coin_id") == coin_id:
                    # If there is a match my_portfolios fills crypto_id_object with the data
                    coin_id_exists = True
                    coin_id_object = token
                    coin_id_object_position = position
                    break


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

        all_contents = mongo.db.portfolios.find()
        print("all_contents")
        print("-------")
        print(all_contents)
        for item in all_contents:
            print(item)

        # default found_portfolio_user = None
        find_portfolio_user = None
        # If the portfolio exists, get username for comparison
        if user_portfolio_contents is not None:
            find_portfolio_user = mongo.db.portfolios.find_one(
                {"username": session["user"]}
            )["username"]

        # If the portfolio can't be found, then create it
        if user_portfolio_contents is None:
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
            mongo.db.portfolios.insert_one(my_portfolios)  # WORKS

        # If the username matches a document but is the first transaction of 
        # the coin it adds a new instance in the array
        elif find_portfolio_user == username and coin_id_exists == False:
            # get object _id
            _id = user_portfolio_contents["_id"]
            # Get portfolios (called by id) - this is a list
            portfolio_contents = user_portfolio_contents["id"]
            portfolio_contents.append({
                    "coin_id": coin_id,
                    "holdings": quantity,
                    "value": value,
                    "grand_total": total,
                    "profit_loss": profit_loss
            })
            mongo.db.portfolios.update({'_id': _id}, {"$set": {"id": portfolio_contents}})  # WORKS
            
        # If both the username and the coin_id make a match then the new data is updated with the old records
        elif find_portfolio_user == username and coin_id_exists == True:
            # get object _id
            _id = user_portfolio_contents["_id"]
            # Get portfolios (called by id) - this is a list
            portfolio_contents = user_portfolio_contents["id"]

            # Calculate new values
            updated_holdings = float(quantity) + float(coin_id_object.get("holdings"))
            updated_value = float(price) * float(coin_id_object.get("holdings"))
            # Need to figure out how to get price
            updated_total = float(total) + float(coin_id_object.get("grand_total"))
            updated_profit = float(coin_id_object.get("value")) - float(coin_id_object.get("grand_total"))
            
            # Buy and stake orders update the the holdings and grand_total by adding the users new order to the records
            if type in ["Buy", "Staking"]:
                # Get portfolios (called by id) - this is a 
                # list - update only coin specific item
                portfolio_contents[coin_id_object_position] = {
                    "coin_id": coin_id,
                    "holdings": updated_holdings,
                    "value": updated_value,
                    "grand_total": updated_total,
                    "profit_loss": updated_profit
                }
                mongo.db.portfolios.update({'_id': _id}, {"$set": {"id": portfolio_contents}})
                
            # Sell orders subtract the holdings from quantity and the total invested by the returns
            elif type == "Sell":
                sell_holdings = float(coin_id_object.get("holdings")) - float(quantity)
                sell_total = float(coin_id_object.get("grand_total")) - float(coin_id_object.get("value"))
                # Get portfolios (called by id) - this is a
                # list - update only coin specific item
                portfolio_contents[coin_id_object_position] = {
                    "coin_id": coin_id,
                    "holdings": sell_holdings,
                    "value": updated_value,
                    "grand_total": sell_total,
                    "profit_loss": updated_profit
                }
                mongo.db.portfolios.update({'_id': _id}, {"$set": {"id": portfolio_contents}})
                

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


# EDIT
@app.route("/edit_record/<record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    if request.method == "POST":

        quantity_edit = request.form.get("quantity_edit")
        per_coin_edit = request.form.get("per_coin_edit")
        total_edit = float(quantity_edit) + float(per_coin_edit)

        update_record = {
            "quantity": float(quantity_edit),
            "per_coin": float(per_coin_edit),
            "date": request.form.get("date_edit"),
            "notes": request.form.get("notes_edit"),
            "total": float(total_edit)
        }
        mongo.db.cryptos.update({"_id": ObjectId(record_id)}, {"$set": {"id": update_record}})
        flash("Record Succesfully Updated")
    
    record = mongo.db.cryptos.find_one({"_id": ObjectId(record_id)})
    return render_template("portfolio.html", record=record)
    # Code institute task manager edit


# DELETE
@app.route("/delete_record/<record_id>", methods=["GET", "POST"])
def delete_record(record_id):
    if request.method == "POST":
        
        mongo.db.cryptos.delete_one({"_id": ObjectId(record_id)})
        flash("Record Successfully Deleted")
        return redirect(url_for("portfolio"))

    delete = mongo.db.cryptos.find_one({"_id": ObjectId(record_id)})
    return render_template("portfolio.html", delete=delete)


@app.route("/delete_all_coin/<record_id>", methods=["GET", "POST"])
def delete_all_coin():
    if request.method == "POST":

        mongo.db.portfolios.delete_one({"_id": ObjectId(record_id)}, {"id": delete_all})

    delete_all = mongo.db.portfolios.delete_one({"_id": ObjectId(record_id)})
    return render_template("portfolio.html", delete_all=delete_all)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)
