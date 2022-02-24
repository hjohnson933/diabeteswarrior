"""If opcode equals c copy the DATA_FILE to the BACKUP_FILE. If opcode equals d copy the BACKUP_FILE to DATA_FILE. Any other opcode return a value error."""

import hashlib
from shutil import copyfile as Cpf
from pathlib import Path as Pth

MODULE_ROOT = Pth(__file__).parent
FOOD_DATA_FILE = MODULE_ROOT.joinpath("food.csv")
MEAL_DATA_FILE = MODULE_ROOT.joinpath("meal.csv")
FOOD_BACKUP_FILE = MODULE_ROOT.joinpath("food.csv.backup")
MEAL_BACKUP_FILE = MODULE_ROOT.joinpath("meal.csv.backup")
MODULE_HELP = {'opcode': 'Use (a) to add a new record, (c) to commit the last record. You can use (d) to delete the last record until it is committed the record. Add a new record is the defult.', 'domain': 'The name of the distributor or manufacture.', 'name': 'The name of the food.', 'portion': 'The individual quantity of food or drink.', 'unit': 'The unit the portion is measured in, grams, ounces slices and so on.', 'calories': 'Energy in kilocalories from the nutritional label.', 'fat': 'The total fat from the nutritional label. the default is in grams.', 'cholesterol': 'The total cholesterol from the nutritional label, the default is in milligrams.', 'sodium': 'The total sodium from the nutritional label, the default is in milligrams.', 'carbohydrate': 'The total carbohydrates from the nutritional label, the default is in grams.', 'protein': 'The total protein from the nutritional label, the default is in grams.'}

if not FOOD_DATA_FILE.exists():
    HEADER_LINE = "'ts', 'domain', 'name', 'portion', 'unit', 'calories', 'fat', 'cholesterol', 'sodium', 'carbohydrate', 'protein'"
    FOOD_DATA_FILE.touch(mode=0o666, exist_ok=True)
    with FOOD_DATA_FILE.open('a', encoding='utf-8') as new_data_file:
        new_data_file.write(F'{HEADER_LINE}\n')

if not FOOD_BACKUP_FILE.exists():
    FOOD_BACKUP_FILE.touch(mode=0o666, exist_ok=True)

if not MEAL_DATA_FILE.exists():
    HEADER_LINE = "'ts', 'calories', 'fat', 'cholesterol', 'sodium', 'carbohydrate', 'protein', 'servings', 'indices'"
    MEAL_DATA_FILE.touch(mode=0o666, exist_ok=True)
    with MEAL_DATA_FILE.open('a', encoding='utf-8') as new_data_file:
        new_data_file.write(F'{HEADER_LINE}\n')

if not MEAL_BACKUP_FILE.exists():
    MEAL_BACKUP_FILE.touch(mode=0o666, exist_ok=True)


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
