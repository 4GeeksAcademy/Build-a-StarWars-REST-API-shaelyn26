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
from models import db, User, Character, Planet, Favorite_Character
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

@app.route('/user', methods=['GET'])
def get_user():
    user = User.query.all()
    user_list = [userData.serialize() for userData in user ]

    return jsonify(user_list), 200


@app.route('/character', methods=['GET'])
def get_character():
    character = Character.query.all()
    character_list = [characterData.serialize() for characterData in character ]

    return jsonify(character_list), 200


@app.route('/planet', methods=['GET'])
def get_planet():
    planet = Planet.query.all()
    planet_list = [planetData.serialize() for planetData in planet ]

    return jsonify( planet_list), 200


@app.route('/Fav_char', methods=['GET'])
def get_fav_character():
    Fav_char_list = Favorite_Character.query.all()
    Fav_Character_list = [Fav_char_data.serialize() for Fav_char_data in Fav_char_list ]

    return jsonify( Fav_Character_list), 200




@app.route('/user', methods=['POST'])
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



@app.route('/person', methods=['POST'])
def handle_person_post():
    data = request.json
    new_person = Character(
        name = data["name"],
        age = data["age"],
        height = data["height"],

    )
    db.session.add(new_person)
    db.session.commit()

    return jsonify(new_person.serialize()), 200

@app.route('/Fav_character', methods=['POST'])
def handle_fav_char_post():
    data = request.json
    new_fav_char = Favorite_Character(
        user_id = data["user_id"],
        character_id = data["character_id"]

    )
    db.session.add(new_fav_char)
    db.session.commit()

    return jsonify(new_fav_char.serialize()), 200








# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


