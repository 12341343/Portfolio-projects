from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def rand():
    if request.method == "GET":
        result = db.session.execute(db.select(Cafe))
        all_cafes = result.scalars().all()

        random_cafe = random.choice(all_cafes)
        return jsonify(cafe={
            "id": random_cafe.id,
            "name": random_cafe.name,
            "map_url": random_cafe.map_url,
            "img_url": random_cafe.img_url,
            "location": random_cafe.location,
            "seats": random_cafe.seats,
            "has_toilet": random_cafe.has_toilet,
            "has_wifi": random_cafe.has_wifi,
            "has_sockets": random_cafe.has_sockets,
            "can_take_calls": random_cafe.can_take_calls,
            "coffee_price": random_cafe.coffee_price,
        })


## HTTP GET - Read Record
@app.route("/all", methods=["GET"])
def all_coffees():
    if request.method == "GET":
        result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
        all_cafes = result.scalars().all()

        # This uses a List Comprehension but you could also split it into 3 lines.
        cf = [{
            "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
        } for cafe in all_cafes]
        return jsonify(cafes=cf)


## HTTP POST - Create Record
@app.route('/search', methods=["GET", "POST"])
def serach():
    query_location = request.args.get("loc")
    result = db.session.execute(select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        coffee = [{
            "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
        } for cafe in all_cafes]
        return jsonify(cafes=coffee)
    else:
        return jsonify(error={"Not found": "Specified city is not found"})


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        map_url = request.form["map_url"]
        print(name)
        user = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(Success={"Success": 'successfully entered parameters.'})


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update(cafe_id):
    new_price = request.args.get("new_price")
    print(new_price)

    seleceted_cafe = db.get_or_404(Cafe, cafe_id)
    if seleceted_cafe:
        seleceted_cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200

    else:
        return jsonify(Eror={"Not found": "Bad input, try again."})


## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def delete_auth(cafe_id):
    api_key = request.args.get("api-key")
    seleceted_cafe = db.get_or_404(Cafe, cafe_id)
    if api_key == "TopSecretAPIKey":
        if seleceted_cafe:
            db.session.delete(seleceted_cafe)
            db.session.commit()
            return jsonify(Success={"Deleted": "Your entry has deleted "})
        else:
            return jsonify(id={"ERROR": "ID error, try againg with correct id number."})
    else:
        return jsonify(Error={"Please try again": "Try again."})


if __name__ == '__main__':
    app.run(debug=True)
