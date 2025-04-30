import enum
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Favorites_Types(enum.Enum):
    planet = 1
    people = 2
    vehicles = 3
    film = 4
    user= 'user'


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.first_name,
            "lastname": self.last_name,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            #"favorites":self.favorites
            "favoriteCount": len(self.favorites)
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "favoriteCount": len(self.favorites)
        }


class Favorite(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Favorites_Types] = mapped_column(Enum(Favorites_Types), nullable=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    planet: Mapped[Planet] = relationship(back_populates="favorites")
    people_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"), nullable=True)
    people: Mapped[People] = relationship(back_populates="favorites")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped[User] = relationship(back_populates="favorites")

    def serialize(self):
        
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id":self.people_id,
            "planet_id": self.planet_id,
            "type": self.type.name 

        }
