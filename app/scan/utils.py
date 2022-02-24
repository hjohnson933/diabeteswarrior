"""If opcode equals c copy the DATA_FILE to the BACKUP_FILE. If opcode equals d copy the BACKUP_FILE to DATA_FILE. Any other opcode return a value error."""

from dataclasses import dataclass
import hashlib
from shutil import copyfile as Cpf
from pathlib import Path as Pth

MODULE_ROOT = Pth(__file__).parent
SCAN_DATA_FILE = MODULE_ROOT.joinpath("food.csv")
SCAN_BACKUP_FILE = MODULE_ROOT.joinpath("food.csv.backup")
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
    'limit': {'min': 55, 'max': 250},
    'target': {'min': 70, 'max': 180},
    'my_target': {'min': 85, 'max': 120},
    'meal': {'ideal': 180, 'good': 250, 'bad': 270}
}

if not SCAN_DATA_FILE.exists():
    HEADER_LINE = '"ts","message","notes","bolus","bolus_u","basal","basal_u","food","carbohydrate","exercise","medication","glucose","trend","lower_limit","upper_limit"'
    SCAN_DATA_FILE.touch(mode=0o666, exist_ok=True)
    with SCAN_DATA_FILE.open('a', encoding='utf-8') as new_data_file:
        new_data_file.write(F'{HEADER_LINE}\n')

if not SCAN_BACKUP_FILE.exists():
    SCAN_BACKUP_FILE.touch(mode=0o666, exist_ok=True)


def archived_status(data_file, backup_file) -> bool:
    df_hash = hashlib.sha256(data_file.read_bytes()).hexdigest()
    bf_hash = hashlib.sha256(backup_file.read_bytes()).hexdigest()
    return df_hash == bf_hash


def backup_restore(opcode, data_file, backup_file) -> str:
    if archived_status(data_file, backup_file):
        return 'The data file is already archived.'
    if opcode == 'c':
        Cpf(data_file, backup_file)
        return 'The data file was successfully archived.'
    if opcode == 'd':
        Cpf(backup_file, data_file)
        return 'The data file was restored successfully.'
    return 'Opecode must be "c" or "d".'


@dataclass
class Records:
    ...
