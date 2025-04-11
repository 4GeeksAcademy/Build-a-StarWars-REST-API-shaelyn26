"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite_Character, Favorite_Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])            # <-- USER get ----> this is an endpoint aka the route -->
def get_user():
    user = User.query.all()
    user_list = [userData.serialize() for userData in user ]

    return jsonify(user_list), 200


@app.route('/character', methods=['GET'])           # <---CHARACTER get--->
def get_character():
    character = Character.query.all()
    character_list = [characterData.serialize() for characterData in character ]

    return jsonify(character_list), 200


@app.route('/character/<int:character_id>', methods=['GET'])           # <--- SINGLE CHARACTER get--->
def get_single_character(character_id):
    if not character:
        return jsonify({"Error Message"})
    character = Character.query.filter_by(id=character_id).first()              # User.query.filter_by(id=user_id).one_or_none()

    return jsonify(character.serialize()), 200


@app.route('/planets', methods=['GET'])              # <---PLANETS get--->
def get_planets():
    planets = Planet.query.all()
    planets_list = [planetsData.serialize() for planetsData in planets ]

    return jsonify( planets_list), 200

@app.route('/fav_planet', methods=['GET'])                # <---FAV PLANET get--->
def get_fav_planet():
    all_fav_planets = Favorite_Planet.query.all()
    fav_planets_list = [fav_planet_data.serialize() for fav_planet_data in all_fav_planets ]

    return jsonify(fav_planets_list), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])              # <--- SINGLE PLANET get--->
def get_single_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()

    return jsonify(planet.serialize()), 200


@app.route('/fav_char', methods=['GET'])                # <---FAV CHARACTER get--->
def get_fav_character():
    favorite_characters = Favorite_Character.query.all()
    fav_character_list = [Fav_char_data.serialize() for Fav_char_data in favorite_characters ]

    return jsonify( fav_character_list), 200

#   <-------------POST methods -------------->

@app.route('/user', methods=['POST'])               # <-------USER post-------->
def handle_user_post():
    data = request.json
    new_user = User(
        email = data["email"],
        password = data["password"],
        is_active = data.get("is_active")

    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 200



@app.route('/character', methods=['POST'])             # <------CHARACTER post------>
def handle_character_post():
    data = request.json
    new_person = Character(
        name = data["name"],
        age = data["age"],
        height = data["height"],

    )
    db.session.add(new_person)
    db.session.commit()

    return jsonify(new_person.serialize()), 200


@app.route('/planet', methods=['POST'])                 # <------PLANET post------->
def handle_planet_post():
    data = request.json
    new_planet = Planet(
        name = data["name"],
        population = data["population"],
        mass = data["mass"],
        is_habitable = data["is_habitable"],
        temperature = data["temperature"],

    )
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 200

@app.route('/fav_planet', methods=['POST'])                  # <-------FAV PLANET post-------->
def handle_fav_planet_post():
    data = request.json
    new_fav_planet = Favorite_Planet(
        user_id = data["user_id"],
        planet_id = data["planet_id"]

    )
    db.session.add(new_fav_planet)
    db.session.commit()

    return jsonify(new_fav_planet.serialize()), 200

@app.route('/fav_character', methods=['POST'])                  # <-------FAV CHARACTER post-------->
def handle_fav_char_post():
    data = request.json
    new_fav_char = Favorite_Character(
        user_id = data["user_id"],
        character_id = data["character_id"]

    )
    db.session.add(new_fav_char)
    db.session.commit()

    return jsonify(new_fav_char.serialize()), 200



# <-----DELETE method---->

@app.route('/fav_planet/<int:fav_planet_id>', methods=['DELETE'])              # <--- Favorite PLANET delete--->
def delete_fav_planet(fav_planet_id):
                    # User.query.filter_by(id=user_id).one_or_none()
    planet = Favorite_Planet.query.get(fav_planet_id)
    planet_json = planet.serialize()
    db.session.delete(planet)
    db.session.commit()
    response = {
        "message": "favorite planet was deleted",
        "planet": planet_json    
        }
    return jsonify(response), 200



@app.route('/fav_character/<int:fav_character_id>', methods=['DELETE'])              # <--- FAVORITE character delete--->
def delete_fav_character(fav_character_id):
                    # User.query.filter_by(id=user_id).one_or_none()
    character = Favorite_Character.query.get(fav_character_id)
    print(character, "this is my character!!!!")
    character_json = character.serialize()
    db.session.delete(character)
    db.session.commit()
    response = {
        "message": "favorite character was deleted",
        "character": character_json    
        }
    return jsonify(response), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


