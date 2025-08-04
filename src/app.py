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
from models import db, User
from sqlalchemy import select

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from models import Estudiantes

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace("postgres://", "postgresql://")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# -----------------ENDPOINTS----------------------------


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    print("email: " + email, "Password: " + password)

    # ------consulta en la tabla "User" ↓↓ donde el "email" ↓↓ coincida con el introducido
    query_user = db.session.execute(select(User).where(User.email == email)).scalar_one_or_none()
    print(query_user)
    # si devuelve "None", es porque no encuentra dicho usuario, entonces podemos tratar el error.

    if query_user is None:
        return jsonify({"msg": "email does not exist"}), 404

    # --- si el "email" ↓↓ o el "password" ↓↓ no coincide con la bd, lanza el error
    if email != query_user.email or password != query_user.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/favorites", methods=["GET"])
@jwt_required()  # ← esto se llama "decorador", se coloca entre la ruta y la función, y es como el "segurata"
def protected():
    # Access the identity of the current user with get_jwt_identity
    email = get_jwt_identity()
    print(email)

    query_user = db.session.execute(select(User).where(User.email == email)).scalar_one_or_none()
    print(query_user.serialize())

    # Después, podemos traer los favoritos del usuario:
    user_favorites = query_user.all_user_favorites()
    print(user_favorites)

    return jsonify(logged_in_as=email, favorites=user_favorites), 200


@app.route("/", methods={"GET"})
# definimos la ruta y el endpoint (GET, POST, DELETE...)
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/people", methods={"GET"})
# definimos la ruta y el endpoint (GET, POST, DELETE...)
def hello_world2():
    return "<p>Hello, World!</p>"


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/user", methods=["GET"])
def handle_hello():

    response_body = {"msg": "Hello, this is your GET /user response "}

    return jsonify(response_body), 200


@app.route("/students", methods=["GET"])
def get_all_students():

    # ↓↓↓ Consultar todos los registros de una tabla, modelo o entidad
    all_students = db.session.execute(select(Estudiantes)).scalars().all()
    # ↓↓↓ Se encarga de procesar la info en un formato legible para devs
    results = list(map(lambda item: item.serialize(), all_students))

    response_body = {"msg": "ok", "results": results}

    return jsonify(response_body), 200


@app.route("/students/<int:id>", methods=["GET"])
def get_one_students(id):
    print(id)

    student = db.session.get(Estudiantes, id)
    print(student)

    if student is None:
        return jsonify({"msg": "El estudiante no existe"}), 404

    response_body = {"msg": "ok", "result": student.serialize}

    return jsonify(response_body), 200


# para levantar el puerto sería el comando $ pipenv run python app.py
# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
