"""Scan Dash Application Interfaces"""
from sqlalchemy import Integer, Boolean, Column, DateTime, Numeric, Text, REAL
from .assets.utils import Base


class Scan(Base):
    __tablename__ = 'scan'

    index = Column(Integer, primary_key=True)
    ts = Column(DateTime)
    message = Column(Integer)
    notes = Column(Text)
    glucose = Column(Integer)
    trend = Column(Integer)
    bolus = Column(Boolean)
    bolus_u = Column(Integer)
    basal = Column(Boolean)
    basal_u = Column(Integer)
    food = Column(Boolean)
    carbohydrate = Column(Integer)
    medication = Column(Boolean)
    exercise = Column(Boolean)
    lower_limit = Column(REAL)
    upper_limit = Column(REAL)
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
