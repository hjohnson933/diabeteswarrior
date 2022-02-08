"""Scan Records"""
__cryptonym__ = "scan"
__version__ = "0.1.0"

import hashlib
import logging
from dataclasses import asdict, astuple, dataclass, fields
from pathlib import Path as P
from shutil import copyfile

MODULE_ROOT = P(__file__).parent
DATA_FILE = MODULE_ROOT.joinpath(f"{__cryptonym__}.csv")
BACK_UP_FILE = MODULE_ROOT.joinpath(f"{__cryptonym__}.csv.backup")
LOG_FILE = MODULE_ROOT.joinpath(f"{__cryptonym__}.log")
MODULE_HELP = {
    'opcode': 'Use (a) to add a new record, (c) to commit the last record. You can use (d) to delete the last record until it is committed the record.',
    'message': '-3 is Glucose Low, -2 is glucose going low, -2 is my glucose low alert, 0 is no message (the default) 1 is my high alert, 2 is going high and 3 is glucose is high.',
    'notes': 'Any extra comment you want to add.',
    'bolus_u': 'The number of units taken to cover or correct your blood sugar.',
    'basal_u': 'The number of units taken to replace insulin overnight, when you are fasting or between meals.',
    'carbohydrate': 'The number of carbohydrates in grams for the meal or snack.',
    'exercise': 'Set to true if you are marking this as a exercise event.',
    'medication': 'Set to true if you are marking this as a medication event.',
    'glucose': 'Blood sugar in milligrams per deciliter.',
    'trend': 'Indicates direction and velocity of change for your glucose level. Values are -2 if the arrow is pointing down, -1 if it down and right, 0 if it is pointing to the right, 1 for up and right and 2 for up.'
}
BGL_RANGES = {
    'chart': {'min': 40, 'max': 400},
    'limit': {'min': 55,'max': 250},
    'target': {'min': 70,'max': 180},
    'my_target': {'min': 85,'max': 120},
    'meal': {'ldeal': 180,'good': 250,'bad': 270}
}

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

if not DATA_FILE.exists():
    HEADER_LINE = '"ts","message","notes","bolus","bolus_u","basal","basal_u","food","carbohydrate","exercise","medication","glucose","trend","lower_limit","upper_limit"'
    DATA_FILE.touch(mode=0o666,exist_ok=True)
    logging.info('%s has been created.',DATA_FILE)
    with DATA_FILE.open('a', encoding='utf8') as new_data_file:
        new_data_file.write(F'{HEADER_LINE}\n')

if not BACK_UP_FILE.exists():
    BACK_UP_FILE.touch(mode=0o666,exist_ok=True)
    logging.info('%s has been created.',BACK_UP_FILE)

def enable_record_archive() -> bool:
    """Latch for the write records button."""
    df_hash = hashlib.md5(DATA_FILE.read_bytes()).hexdigest()
    bf_hash = hashlib.md5(BACK_UP_FILE.read_bytes()).hexdigest()
    return df_hash == bf_hash


@dataclass
class Records:
    """Base Class For Scans"""
    message: int
    notes: str
    glucose: int
    t_s: str
    bolus_u: int = 0
    basal_u: int = 0
    carbohydrate: int = 0
    trend: int = 0
    lower_limit: float = -1.0
    upper_limit: float = 1.0
    bolus: bool = False
    basal: bool = False
    food: bool = False
    exercise: bool = False
    medication: bool = False

    def __post_init__(self):
        if self.message not in range(-3, 4):
            raise ValueError("Message must be an integer in the range of -3 to 3.")
        if self.trend not in range(-2, 3):
            raise ValueError("Trend must be an integer in the range of -2 to 2.")
        if self.glucose < 1:
            raise ValueError("Glucose must be a postitve integer.")
        if self.carbohydrate < 0:
            raise ValueError("Carbohydrate must be equal to or greater than 0.")
        if self.bolus_u < 0 or self.basal_u < 0:
            raise ValueError("Insulin must be equal to or greater than 0.")
        if self.bolus_u != 0:
            self.bolus = True
        if self.basal_u != 0:
            self.basal = True
        if self.carbohydrate != 0:
            self.food = True

    @staticmethod
    def records_backup_restore(opcode) -> str:
        """Copy the contents of BACK_UP_FILE to DATA_FILE unless they are already the same."""
        if not enable_record_archive():
            if opcode == 'c':
                copyfile(DATA_FILE, BACK_UP_FILE)
                logging.info('Data file has been copied to the backup file.')
            elif opcode == 'd':
                copyfile(BACK_UP_FILE, DATA_FILE)
                logging.info('The data file has been restored from the back up file.')
        return "The data file and back up file are the same, no operation is needed."

    def record_add(self) -> int:
        """Write new record to database."""
        record = F'{self.t_s},{self.message},"{self.notes}",{self.bolus},{self.bolus_u},{self.basal},{self.basal_u},{self.food},{self.carbohydrate},{self.exercise},{self.medication},{self.glucose},{self.trend},{self.lower_limit},{self.upper_limit}'

        with DATA_FILE.open('a',encoding='utf-8') as data_file:
            hr_data = data_file.write(F"{record}\n")
            logging.info("Recorded %s", record)
            return hr_data
