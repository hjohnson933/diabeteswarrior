"""Meal Records"""
__cryptonym__ = "meal"
__version__ = "0.1.0"

import hashlib
from dataclasses import dataclass
from pathlib import Path as Pth
from shutil import copyfile as Cpf

import arrow as Arw

MODULE_ROOT = Pth(__file__).parent
DATA_FILE = MODULE_ROOT.joinpath(F"{__cryptonym__}.csv")
BACKUP_FILE = MODULE_ROOT.joinpath(F"{__cryptonym__}.csv.backup")

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
    calories: int
    fat: int
    cholesterol: int
    sodium: int
    carbohydrate: int
    protein: int
    servings: list[float]
    indices: list[int]

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
        """Write this record to file."""
        with DATA_FILE.open("a") as data_file:
            hr_data = data_file.write(f'{Arw.now().format("YYYY-MM-DD HH:mm")},{self.calories},{self.fat},{self.cholesterol},{self.sodium},\
                {self.carbohydrate},{self.protein},"{self.servings}","{self.indices}"\n')
            return hr_data
