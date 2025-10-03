from random import choice

from flask import Flask, jsonify, request, render_template
import json
import requests
import random
import os
app = Flask("Boliviaakjonen netavise")

pic_name='item_image.jpg'

PRODUCTS_FILE = "products.json"

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#index:int = 0
@app.route("/")
def index():
    with open(PRODUCTS_FILE, "r") as f:
        products = json.loads(f.read())
    if len(products["products"]) > 1:
        product1 = random.choice(products["products"])
        product2 = random.choice(products["products"])
        while product1 == product2:
            product2 = random.choice(products["products"])
        return render_template("couple.html", product1=product1, product2=product2)
    else:
        product = random.choice(products["products"])
        return render_template("single.html", product=product)

@app.route("/order")
def order():
    return render_template("order.html")

@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form["name"]
    seller = request.form["seller"]
    description = request.form["description"]
    classroom = request.form["classroom"]
    contacts = request.form["contacts"]
    price = request.form["price"]
    picture_file = request.files["picture"]


    picture = picture_file.filename
    while os.path.exists(UPLOAD_FOLDER+"/"+picture):
        picture = str(random.randint(0,9999))+picture
    picture_file.save(os.path.join(app.config['UPLOAD_FOLDER'], picture))

    new_data={"name": name,
        "seller": seller,
        "description": description,
        "classroom": classroom,
        "contacts": contacts,
        "price": price,
        "picture": picture
    }
    with open(PRODUCTS_FILE, "r") as f:
        products = json.loads(f.read())
        products["products"].append(new_data)
        with open(PRODUCTS_FILE, "w") as l:
            json.dump(products, l, indent=4)
        return "Takk for bestilling!"

@app.errorhandler(Exception)
def error(e):
    return f"Det skjedde noe galt med exitcode {e}"


app.run(debug=True)