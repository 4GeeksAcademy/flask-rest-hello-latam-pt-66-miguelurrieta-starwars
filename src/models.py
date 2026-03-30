import os
import sys
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import create_engine
from eralchemy2 import render_er


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="user")


class Character(Base):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250))

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="character")


class Planet(Base):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))

    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="planet")


class Favorite(Base):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    character_id: Mapped[int | None] = mapped_column(
        ForeignKey('character.id'), nullable=True)
    planet_id: Mapped[int | None] = mapped_column(
        ForeignKey('planet.id'), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    character: Mapped["Character"] = relationship(
        "Character", back_populates="favorites")
    planet: Mapped["Planet"] = relationship(
        "Planet", back_populates="favorites")


try:
    render_er(Base, 'diagram.png')
    print("¡Éxito! Diagrama de Star Wars generado.")
except Exception as e:
    print("Error generando el diagrama")
    raise e
