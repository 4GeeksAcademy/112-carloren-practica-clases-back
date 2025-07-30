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

from models import Estudiantes

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://"
    )
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
