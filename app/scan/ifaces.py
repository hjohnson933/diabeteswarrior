"""Scan Data Interfaces"""
from typing import Any

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Numeric, Text, REAL, create_engine
from sqlalchemy.orm import declarative_base

Engine = create_engine('postgresql://hjohnson933:__46_LITTLE_barbados_LATE_76__@git.house.lan:5432/hjohnson933')
Base: Any = declarative_base()


class Scan(Base):
    __tablename__ = 'scan'

    index = Column(BigInteger, primary_key=True)
    ts = Column(DateTime)
    message = Column(BigInteger)
    notes = Column(Text)
    glucose = Column(BigInteger)
    trend = Column(BigInteger)
    bolus = Column(Boolean)
    bolus_u = Column(BigInteger)
    basal = Column(Boolean)
    basal_u = Column(BigInteger)
    food = Column(Boolean)
    carbohydrate = Column(BigInteger)
    medication = Column(Boolean)
    exercise = Column(Boolean)
    lower_limit = Column(REAL)
    upper_limit = Column(REAL)
    level_0 = Column(BigInteger)


class Config(Base):
    __tablename__ = 'config'

    id = Column(BigInteger, primary_key=True)
    ts = Column(DateTime)
    chart_min = Column(BigInteger, default=40)
    chart_max = Column(BigInteger, default=400)
    limit_min = Column(BigInteger, default=55)
    limit_max = Column(BigInteger, default=250)
    target_min = Column(BigInteger, default=70)
    target_max = Column(BigInteger, default=180)
    my_target_min = Column(BigInteger)
    my_target_max = Column(BigInteger)
    meal_ideal = Column(BigInteger, default=180)
    meal_good = Column(BigInteger, default=250)
    meal_bad = Column(BigInteger, default=270)
    my_target_weight = Column(Numeric)
    my_target_bmi = Column(Numeric)
