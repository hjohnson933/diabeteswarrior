"""Health Data Interfaces"""
from sqlalchemy import Integer, Boolean, Column, DateTime, Numeric, REAL
from .assets.utils import Base


class Health(Base):
    __tablename__ = 'health'

    index = Column(Integer, primary_key=True)
    ts = Column(DateTime)
    level_0 = Column(Integer)
    po_pulse = Column(Integer)
    po_ox = Column(Integer)
    weight = Column(REAL)
    fat = Column(REAL)
    bpc_pulse = Column(Integer)
    bpc_systolic = Column(Integer)
    bpc_diastolic = Column(Integer)
    bpc_ihb = Column(Boolean)
    bpc_hypertension = Column(Integer, default=0)
    temperature = Column(REAL)


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
