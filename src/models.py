from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    age: Mapped[str] = mapped_column(String(5), nullable=True)
    height: Mapped[str] = mapped_column(String(5), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "height": self.height,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(nullable=True)
    mass: Mapped[int] = mapped_column(nullable=False)
    temperature: Mapped[int] = mapped_column(nullable=False)
    is_habitable: Mapped[bool] =mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "poplation": self.population,
            "mass": self.mass,
            "temperature": self.temperature,
            "is_habitable": self.is_habitable
            # do not serialize the password, its a security breach
        }


class Favorite_Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    user: Mapped["User"] = relationship("User")
    character: Mapped["Character"] = relationship("Character")
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.email,
            "character": self.character.name
            # do not serialize the password, its a security breach
        }