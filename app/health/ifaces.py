"""Health Data Interfaces"""
from typing import Any

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Numeric, REAL, create_engine
from sqlalchemy.orm import declarative_base

Engine = create_engine('postgresql://hjohnson933:__46_LITTLE_barbados_LATE_76__@git.house.lan:5432/hjohnson933')
Base: Any = declarative_base()


class Health(Base):
    __tablename__ = 'health'

    index = Column(BigInteger, primary_key=True)
    ts = Column(DateTime)
    level_0 = Column(BigInteger)
    po_pulse = Column(BigInteger)
    po_ox = Column(BigInteger)
    weight = Column(REAL)
    fat = Column(REAL)
    bpc_pulse = Column(BigInteger)
    bpc_systolic = Column(BigInteger)
    bpc_diastolic = Column(BigInteger)
    bpc_ihb = Column(Boolean)
    bpc_hypertension = Column(BigInteger, default=0)
    temperature = Column(REAL)


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
