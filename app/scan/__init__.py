"""Scan Records"""

__cryptonym__ = 'scan'
__version__ = '0.1.0'

import hashlib
from dataclasses import dataclass
from pathlib import Path as Pth
from shutil import copyfile as Cpf

import arrow as Arw

MODULE_ROOT = Pth(__file__).parent
DATA_FILE = MODULE_ROOT.joinpath(F"{__cryptonym__}.csv")
BACKUP_FILE = MODULE_ROOT.joinpath(F"{__cryptonym__}.csv.backup")
BGL_RANGES = {"chart": {"min": 40, "max": 400},
              "limit": {"min": 55, "max": 250},
              "target": {"min": 70, "max": 180},
              "my_target": {"min": 85, "max": 120},
              "meal": {"ideal": 180, "good": 250, "bad": 270}}

if not DATA_FILE.exists():
    HEADER_LINE = '"ts","message","notes","bolus","bolus_u","basal","basal_u","food","carbohydrate","exercise","medication","glucose",\
        "trend","lower_limit","upper_limit"'
    DATA_FILE.touch(mode=0o666, exist_ok=True)
    with DATA_FILE.open('a', encoding='utf-8') as new_data_file:
        new_data_file.write(F'{HEADER_LINE}\n')

if not BACKUP_FILE.exists():
    BACKUP_FILE.touch(mode=0o666, exist_ok=True)


def enable_record_archive() -> bool:
    df_hash = hashlib.sha256(DATA_FILE.read_bytes()).hexdigest()
    bf_hash = hashlib.sha256(BACKUP_FILE.read_bytes()).hexdigest()
    return df_hash == bf_hash


@dataclass
class Records:
    ts: str
    message: int
    notes: str
    bolus: bool
    bolus_u: int
    basal: bool
    basal_u: int
    food: bool
    carbohydrate: int
    exercise: bool
    medication: bool
    glucose: int
    trend: int
    lower_limit: int
    upper_limit: int

    def __post_init__(self) -> None:
        if self.message not in range(-3, 4):
            raise ValueError("Message must be a integer in the range of -3 to 3.")
        if self.trend not in range(-2, 3):
            raise ValueError("Trend must be a integer in the range of -2 to 2.")
        if self.glucose < 1:
            raise ValueError("Glucose must be positive integer.")

    @staticmethod
    def records_backup_restore(opcode) -> str:
        """If opcode equals c copy the DATA_FILE to the BACKUP_FILE. If opcode equals d copy the BACKUP_FILE to DATA_FILE. Any other
        opcode return a value error."""
        if not enable_record_archive():
            if opcode == 'c':
                Cpf(DATA_FILE, BACKUP_FILE)
                return 'The data file was successfully backed up.'
            elif opcode == 'd':
                Cpf(BACKUP_FILE, DATA_FILE)
                return 'The data file was restored successfully.'
            return 'Incorrect opecode given, send "c" or "d".'

    def record_add(self) -> int:
        """"Write new record to the database and return the number of bytes written."""
        hr_data = F'{Arw.now().format("YYYY-MM-DD HH:mm")},'
        with DATA_FILE.open('a', encoding='utf-8') as data_file:
            hr_data = data_file.write(F'{Arw.now().format("YYYY-MM-DD HH:mm")},{self.message},"{self.notes}",{self.bolus},{self.bolus_u},\
                {self.basal},{self.basal_u},{self.food},{self.carbohydrate},{self.exercise},{self.medication},{self.glucose},{self.trend},\
                    {self.lower_limit},{self.upper_limit}\n')
            return hr_data
