"""Food Records"""
__cryptonym__ = "food"
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
    'opcode': 'Use (a) to add a new record, (c) to commit the last record. You can use (d) to delete the last record until it is committed the record. Add a new record is the defult.',
    'domain':'The name of the distributor or manufacture.',
    'name':'The name of the food.',
    'portion':'The number of the portions of this food your eating.',
    'unit':'The unit the portion is measured in, grams, ounces slices, servings, packages or Meal.',
    'calories':'Energy in kilocalories from the nutritional label.',
    'fat':'The total fat from the nutritional label. the default is in grams.',
    'cholesterol':'The total cholesterol from the nutritional label, the default is in milligrams.',
    'sodium':'The total sodium from the nutritional label, the default is in milligrams.',
    'carbohydrate':'The total carbohydrates from the nutritional label, the default is in grams.',
    'protein':'The total protein from the nutritional label, the default is in grams.'
}

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

if not DATA_FILE.exists():
    HEADER_LINE = '"ts","domain","name","portion","unit","calories","fat","cholesterol","sodium","carbohydrate","protein"'
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


class Records:
    """Food Record"""
    domain: str
    name: str
    portion: str
    unit: str
    calories: int
    fat: int
    cholesterol: int
    sodium: int
    carbohydrate: int
    protein: int
    t_s: str

    def __post_init__(self):
        # todo store only the first letter of the `unit` field with proper capitalization.
        ...

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
        # todo Modify the record to match the class.
        record = F'{self.t_s},"{self.domain}","{self.name}","{self.portion}","{self.unit}",{self.calories},{self.fat},{self.cholesterol},{self.sodium},{self.carbohydrate},{self.protein}'

        with DATA_FILE.open('a',encoding='utf-8') as data_file:
            hr_data = data_file.write(F"{record}\n")
            logging.info("Recorded %s", record)
            return hr_data
