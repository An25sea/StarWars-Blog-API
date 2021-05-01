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
from models import db, User , Person , Planet, Favorite
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
import json

#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config["JWT_SECRET_KEY"]= os.environ.get("JWT_SECRET_KEY")
jwt=JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
     user=User.query.all()
     user = list(map(lambda x: x.serialize(), user))
     return jsonify({"results":user})

    


@app.route("/login", methods=["POST"])
def login():
    email=request.json.get("email", None)
    password=request.json.get("password", None)

    user=User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify ({"message:" "Bad user or password"})

    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token})

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id=get_jwt_identity()
    user=User.query.get(current_user_id)
    return jsonify({"id":user.id, "email":user.email})

@app.route("/createUser", methods=["POST"])
def create_User():
    email=request.json.get("email", None)
    password=request.json.get("password", None)
    name=request.json.get("name", None)
    is_active=request.json.get("is_active", None)
    user=User(email=email, password=password, name=name, is_active=True)
    db.session.add(user)
    db.session.commit()
    return jsonify({"user":"ok"})


@app.route("/person", methods=["GET"])
def People():
    user=Person.query.all()
    user = list(map(lambda x: x.serialize(), user))
    return jsonify({"results":user})

@app.route("/person", methods=["POST"])
def People_agregar():
    name=request.json.get("name", None)
    color_eyes=request.json.get("color_eyes",None)
    color_hair=request.json.get("color_hair",None)
    gender=request.json.get("gender",None)
    birth=request.json.get("birth",None)
    height=request.json.get("height",None)
    color_skin=request.json.get("color_skin",None)
    person=Person(name=name, color_eyes=color_eyes, color_hair=color_hair, gender=gender,birth=birth,height=height,color_skin=color_skin)
    db.session.add(person)
    db.session.commit()
    #user=json.loads(name, color_ojos, color_cabello,gender)
    return jsonify({"people":"ok"})

@app.route("/planet", methods=["GET"])
def Planet_get():
    planet=Planet.query.all()
    planet = list(map(lambda x: x.serialize(), planet))
    return jsonify({"results":planet})

@app.route("/planet", methods=["POST"])
def Planet_agregar():
    name=request.json.get("name",None)
    diameter=request.json.get("diameter",None)
    rotation=request.json.get("rotation",None)
    population=request.json.get("population",None)
    terrain=request.json.get("terrain",None)
    orbital=request.json.get("orbital",None)
    gravity=request.json.get("gravity",None)
    planet=Planet(name=name, diameter=diameter, rotation=rotation, population=population, terrain=terrain,orbital=orbital,gravity=gravity)
    db.session.add(planet)
    db.session.commit()
    #user=json.loads(name, color_ojos, color_cabello,gender)
    return jsonify({"planet":"ok"})

@app.route("/favorite", methods=["POST"])
@jwt_required()
def agregar_favorite():
    id_user=request.json.get("id_user",None)
    id_planet=request.json.get("id_planet",None)
    id_person=request.json.get("id_person",None)
    favorite=Favorite(user_id=id_user, planet_id=id_planet, person_id=id_person)
    db.session.add(favorite)
    db.session.commit()
    #user=json.loads(name, color_ojos, color_cabello,gender)
    return jsonify({"Favorite":"Add"})


@app.route("/favorite", methods=["GET"])
@jwt_required()
def favorite():
    favorite=Favorite.query.all()
    favorite = list(map(lambda x: x.serialize(), favorite))
    return jsonify({"Results:":favorite})
#return 'Response for the POST todo'

@app.route('/favorite/<int:position>', methods=['DELETE'])
@jwt_required()
def delete_favorite(position):
    favorite = Favorite.query.get(position)
    if favorite is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"favorite":"Was Delete"})
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
