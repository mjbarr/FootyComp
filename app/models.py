from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")

    picks = relationship("Pick", back_populates="user")
    jokers = relationship("Joker", back_populates="user")


class Fixture(Base):
    __tablename__ = "fixtures"

    id = Column(Integer, primary_key=True)
    season = Column(Integer, default=1, nullable=False)
    week = Column(Integer, default=1, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    odds = Column(String, nullable=False)


class Pick(Base):
    __tablename__ = "picks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fixture_id = Column(Integer, ForeignKey("fixtures.id"))
    joker = Column(Integer, default=0)  # 0=none,1=first joker,2=second

    user = relationship("User", back_populates="picks")
    fixture = relationship("Fixture")


class OddsMapping(Base):
    __tablename__ = "odds_mapping"

    id = Column(Integer, primary_key=True)
    odds = Column(String, nullable=False, unique=True)
    points = Column(Integer, nullable=False)


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    fixture_id = Column(Integer, ForeignKey("fixtures.id"), unique=True)
    home_score = Column(Integer, nullable=False)
    away_score = Column(Integer, nullable=False)

    fixture = relationship("Fixture")


class Joker(Base):
    __tablename__ = "jokers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pick_id = Column(Integer, ForeignKey("picks.id"))
    used_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="jokers")
    pick = relationship("Pick")
