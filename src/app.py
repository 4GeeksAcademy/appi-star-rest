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
from models import db, User, Favorite, Favorites_Types, Planet, People
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"mensaje": "User not found"}), 404
    return jsonify(user.serialize()), 200


@app.route("/favorites/user", methods=["GET"])
def handle_get_user_favorite():
    user = User.query.first()  # Metodo para obtener el primer usuario
    if not user:
        return jsonify({"msg": "User not found"}), 404

    favorites = Favorite.query.filter_by(
        user_id=1
    ).all()  # Metodo para obtener todos los favoritos de un usuario en concreto
    return jsonify(
        [fav.serialize() for fav in favorites]
    ), 200


@app.route('/planet', methods=['GET'])
def handle_get_planets():
    planet = Planet.query.all()
    planet = list(map(lambda p: p.serialize(), planet))
    return jsonify(planet)


@app.route('/people', methods=['GET'])
def handle_get_people():
    people = People.query.all()
    people = list(map(lambda p: p.serialize(), people))
    return jsonify(people)

# @app.route('/favorites/<item_type>/<int:item_id>', methods=['POST'])
# def handle_post_favorite(item_type,item_id):
 #   new_favorite=Favorite()
  #  if item_type=="people":
   #     new_favorite.type=Favorites_Types.people
    #    new_favorite.people_id=item_id
    # elif item_type=="planet":
    #   new_favorite.type=Favorites_Types.planet
    #  new_favorite.planet_id=item_id
    # else:
    #   return jsonify({"msg":"Favorite Invalid"}),404

    # db.session.add(new_favorite)
    # db.session.commit()
   # return jsonify({"msg": "successfully created","favorite":new_favorite.serialize()}),201


@app.route("/favorites/people/<int:people_id>", methods=["GET"])
def handle_get_favorite_people(people_id):
    favorite_people = Favorite.query.filter_by(
        type=Favorites_Types.people,
        people_id=people_id
    ).all()
    if not favorite_people:
        return jsonify({"msg": "Favorite people not found"}), 404

    return jsonify([favorite_people.serialize() for favorite_people in favorite_people]), 200


@app.route("/favorites/planet/<int:planet_id>", methods=["GET"])
def handle_get_favorite_planet(planet_id):
    favorite_planet = Favorite.query.filter_by(
        type=Favorites_Types.planet,
        planet_id=planet_id
    ).all()
    if not favorite_planet:
        return jsonify({"msg": "Favorite planet not found"}), 404

    return jsonify([favorite_planet.serialize() for favorite_planet in favorite_planet]), 200


@app.route("/favorites/<int:userId>", methods=["GET"])
def handle_get_favorites(userId):
    user_favorites = Favorite.query.filter_by(user_id=1).all()
    user_favorites = list(map(lambda fav: fav.serialize(), user_favorites))
    return jsonify(user_favorites), 200


@app.route('/favorites/<item_type>/<int:item_id>', methods=['DELETE'])
def handle_delete_favorite(item_type, item_id):
    favorite = None
    user = 1
    if item_type == "people":
        favorite = Favorite.query.filter_by(
            user_id=1,
            people_id=item_id
        ).first()
    elif item_type == "planet":
        favorite = Favorite.query.filter_by(
            user_id=1,
            planet_id=item_id
        ).first()
    else:
        return jsonify({"msg": "Favorito invalido"}), 404

    if favorite is  None:
        return jsonify({"msg": "Favorite not found"}), 400

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Successfully deleted"}), 200


@app.route("/favorites/planet/<int:planet_id>", methods=["POST"])
def ad_favorite_planet(planet_id):
    user = User.query.first()  # filtramos para obtener el primer usuario
    new_favorite = Favorite(user_id=1, planet_id=planet_id,type=Favorites_Types.planet)

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite added successfully"}), 200


@app.route("/favorites/people/<int:people_id>", methods=["POST"])
def ad_favorite_people(people_id):
    user = User.query.first()  # filtramos para obtener el primer usuario
    new_favorite = Favorite(user_id=1, people_id=people_id,type=Favorites_Types.people)

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite added successfully"}), 200


# @app.route("/favorites/planet/<int:planet_id>", methods=["DELETE"])
# def delete_favorite_planet(planet_id): 
#     user = User.query.first()  # filtramos para obtener el primer usuario
#     new_favorite = Favorite.query.filter_by(user_id=1, planet_id=planet_id).first()

#     db.session.delete(new_favorite)
#     db.session.commit()
#     return jsonify({"msg": "Favorite delete successfully"}), 200

# @app.route("/favorites/people/<int:people_id>", methods=["DELETE"])
# def delete_favorite_people(people_id):
#     user = User.query.first()  # filtramos para obtener el primer usuario
#     new_favorite = Favorite.query.filter_by(user_id=1, people_id=people_id).first()

#     db.session.delete(new_favorite)
#     db.session.commit()
#     return jsonify({"msg": "Favorite delete successfully"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
