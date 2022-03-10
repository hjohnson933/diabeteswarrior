"""Meal Dash Application Interfaces."""
from sqlalchemy import Integer, Column, DateTime, Numeric, REAL, TEXT
from .assets.utils import Base


class Meals(Base):
    """Meal Model."""

    __tablename__ = 'meal'

    index = Column(Integer, primary_key=True)
    ts = Column(DateTime)
    level_0 = Column(Integer)
    calories = Column(REAL)
    fat = Column(REAL)
    cholesterol = Column(REAL)
    sodium = Column(REAL)
    carbohydrate = Column(REAL)
    protein = Column(REAL)
    serving = Column(TEXT)
    indices = Column(TEXT)


class Foods(Base):
    """Food Model."""

    __tablename__ = 'food'

    index = Column(Integer, primary_key=True)
    ts = Column(DateTime)
    level_0 = Column(Integer)
    domain = Column(TEXT)
    name = Column(TEXT)
    portion = Column(TEXT)
    unit = Column(TEXT)
    calories = Column(Integer)
    fat = Column(Integer)
    cholesterol = Column(Integer)
    sodium = Column(Integer)
    carbohydrate = Column(Integer)
    protein = Column(Integer)


class Config(Base):
    """User Configuration Model."""

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
