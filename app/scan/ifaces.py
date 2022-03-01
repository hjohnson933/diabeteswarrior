"""Scan Data Interfaces"""
from dataclasses import dataclass
from typing import Any

from sqlalchemy import (BigInteger, Boolean, Column, DateTime, Numeric, Text,
                        create_engine)
from sqlalchemy.orm import declarative_base

Engine = create_engine('postgresql://hjohnson933:__46_LITTLE_barbados_LATE_76__@git.house.lan:5432/hjohnson933')
Base: Any = declarative_base()

BTN_DICT = {
    'scope': [('Last 24 hours', 24), ('Last 14 days', 336), ('Last 90 days', 2160)],
    'event': [('No Special Event', None), ('Bolus Insulin', None), ('Basal Insulin', None), ('Meal', None), ('Medication', None), ('Execrise', None)],
    'message': [('Is high', 3), ('Is going high', 2), ('My high alarm', 1), ('No alarm', 0), ('My low alarm', -1), ('Is going low', -2), ('Is low', -3)],
    'trend': [('Pointing up', 2), ('Pointing up and right', 1), ('Pointing right', 0), ('Pointing down and right', -1), ('Pointing down', -2)]
    }


@dataclass
class Record:
    ts: str
    message: int
    notes: str
    glucose: int
    trend: int
    bolus: bool
    bolus_u: int
    basal: bool
    basal_u: int
    food: bool
    carbohydrate: int
    medication: bool
    exercise: bool
    lower_limit: int
    upper_limit: int

    def __post_init__(self):
        if self.message not in range(-3, 4):
            raise ValueError("Message must be in the range of -3 to 3.")
        if self.trend not in range(-2, 3):
            raise ValueError("Trend must be in the range of -2 to 2.")
        if self.glucose < 1:
            raise ValueError("Glucose must be a positive BigInteger.")

    def record_add(self, data_file) -> int:
        with data_file.open('a', encoding='utf-8') as data:
            hr_data = data.write(f'{self.ts},{self.message},"{self.notes}",{self.bolus},{self.bolus_u},{self.basal},{self.basal_u},{self.food},{self.carbohydrate},{self.exercise},{self.medication},{self.glucose},{self.trend},{self.lower_limit},{self.upper_limit}\n')
        return hr_data


class Records(Base):
    __tablename__ = 'scan'

    id = Column(BigInteger, primary_key=True)
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
    lower_limit = Column(BigInteger)
    upper_limit = Column(BigInteger)


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
