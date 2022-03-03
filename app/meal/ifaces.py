"""Meal Data Interfaces"""
from typing import Any

from sqlalchemy import Integer, Column, DateTime, Numeric, REAL, create_engine, ARRAY
from sqlalchemy.orm import declarative_base

Engine = create_engine('postgresql://hjohnson933:__46_LITTLE_barbados_LATE_76__@git.house.lan:5432/hjohnson933')
Base: Any = declarative_base()


class Meal(Base):
    __tablename__ = 'meal'

    index = Column(Integer, primary_key=True)
    ts = Column(DateTime)
    level_0 = Column(Integer)
    calories = Column(Integer)
    fat = Column(Integer)
    cholesterol = Column(Integer)
    sodium = Column(Integer)
    carbohydrate = Column(Integer)
    protein = Column(Integer)
    servings = Column(ARRAY(REAL))
    indices = Column(ARRAY(Integer))


class Food(Base):
    __tablename__ = 'food'

    index = Column(Integer, primary_key=True)
    ts = Column(DateTime)
    level_0 = Column(Integer)


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    ts = Column(DateTime)
    chart_min = Column(Integer, default=40)
    chart_max = Column(Integer, default=400)
    limit_min = Column(Integer, default=55)
    limit_max = Column(Integer, default=250)
    target_min = Column(Integer, default=70)
    target_max = Column(Integer, default=180)
    my_target_min = Column(Integer)
    my_target_max = Column(Integer)
    meal_ideal = Column(Integer, default=180)
    meal_good = Column(Integer, default=250)
    meal_bad = Column(Integer, default=270)
    my_target_weight = Column(Numeric)
    my_target_bmi = Column(Numeric)
