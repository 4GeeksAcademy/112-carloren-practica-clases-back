from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[List["Favorites"]] = relationship("Favorites", back_populates="user", cascade=("all, delete-orphan"))

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    def all_user_favorites(self):
        results_favorites = list(map(lambda item: item.serialize(), self.favorites))
        print(self.favorites)
        return {
            "id": self.id,
            "email": self.email,
            "favorites": results_favorites,
        }


class Estudiantes(db.Model):
    # clase modelo que se convertirá en tabla. Se escribe en PascalCase y el db.Model lo transformará a snake_case para la tabla
    id: Mapped[int] = mapped_column(primary_key=True)
    # Se van declarando las columnas, y cuál es la primary key
    nombre: Mapped[str] = mapped_column(String(120))
    # El nombre tendrá un límite de 120 caracteres
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    # El email, además, no se podrá repetir (unique) y no podrá estar vacío (nullable)
    direccion: Mapped["Direccion"] = relationship(back_populates="estudiantes")
    # Para relacionar cada estudiante con su dirección. Luego en la tabla dirección tenemos que añadir foreign key

    def serialize(self):
        # "serialize" no es una palabra reservada, pero sí un estandar, es la función para poder devolver un diccionario (Objeto)
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

        # Conforme vayamos creando tablas, podemos correr los comandos "pipenv run migrate, pipenv run upgrade, pipenv run diagram"
        # para que se dibujen las tablas y veamos si se han creado


class Direccion(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    barrio: Mapped[str] = mapped_column(String(120))
    calle: Mapped[str] = mapped_column(String(120))
    parent_id: Mapped[int] = mapped_column(ForeignKey("estudiantes.id"))
    estudiantes: Mapped["Estudiantes"] = relationship(back_populates="direccion")

    def serialize(self):
        return {
            "id": self.id,
            "barrio": self.barrio,
            "calle": self.calle,
            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    nombre: Mapped[str] = mapped_column(String(120))
    color: Mapped[str] = mapped_column(String(120))

    def serialize(self):
        result = {"id": self.id, "nombre": self.nombre, "color": self.color}

        return result
