"""Health Records"""
# pylint: disable=line-too-long
# pylint: disable=invalid-name

__cryptonym__ = 'health'
__version__ = '0.1.0'

import hashlib
import logging
from dataclasses import asdict, astuple, dataclass, field
from pathlib import Path as P
from shutil import copyfile

import arrow as A

MODULE_ROOT = P(__file__).parent
DATA_FILE = MODULE_ROOT.joinpath(F"{__cryptonym__}.csv")
BACK_UP_FILE = MODULE_ROOT.joinpath(F"{__cryptonym__}.csv.backup")
LOG_FILE = MODULE_ROOT.joinpath(F"{__cryptonym__}.log")

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

if not DATA_FILE.exists():
    header_line = '"ts","po_pulse","spox","weight","fat","pulse","systolic","diastolic","ihb","hypertension","temperature"'
    DATA_FILE.touch(mode=0o666,exist_ok=True)
    logging.info('%s has been created.',DATA_FILE)
    with DATA_FILE.open('a', encoding='utf8') as new_data_file:
        new_data_file.write(F'{header_line}\n')

if not BACK_UP_FILE.exists():
    BACK_UP_FILE.touch(mode=0o666,exist_ok=True)
    logging.info('%s has been created.',BACK_UP_FILE)

def enable_record_archive() -> bool:
    """Latch for the write records button."""
    df_hash = hashlib.md5(DATA_FILE.read_bytes()).hexdigest()
    bf_hash = hashlib.md5(BACK_UP_FILE.read_bytes()).hexdigest()
    return df_hash == bf_hash

MODULE_HELP = {
    'opcode': 'Use (a) to add a new record, (c) to commit the last record. You can use (d) to delete the last record until it is committed the record.',
    'po':'Heart rate (pulse) from the pulseoximeter.',
    'spox':'Oxygen saturation level form the pulseoximeter',
    'weight':'Body weight from the Tanita bathroom scale.',
    'fat':'Precentage of body fat from the Tanita bathroom scale.',
    'pulse':'Heart rate (pulse) from the WGNBPW-720 blood presure cuff (Sphygmomanometer).',
    'systolic':'The systolic pressure in mm/mg from the WGNBPW-720 blood presure cuff (Sphygmomanometer).',
    'diastolic':'The diastolic pressure in mm/mg from the WGNBPW-720 blood pressure cuff (Sphygmomanometer).',
    'ihb':'The irregular heart beat indicator from the WGNBPW-720 blood pressure cuff (Sphygmomanometer) 1 for true, 0 is the default.',
    'hypertension':'Hypertension stage from the WGNBPW-720 blood pressure cuff (Sphygmomanometer). 0=No indicator, 1=Pre indicator, 2=Stage I indicator, 3=Stage II indicator',
    'temperature':'Body temperature, any thermometer will do.',
    't_s': 'Timestamp of the record.'
}


@dataclass
# pylint: disable=too-many-instance-attributes
class Records:
    """Base class for health records."""
    po_pulse:int
    spox:int
    weight:float
    fat:float
    pulse:int
    systolic:int
    diastolic:int
    ihb:bool
    hypertension:int
    temperature:float
    t_s:str

    def __post_init__(self) -> None:
        for _ in [self.po_pulse, self.spox, self.systolic, self.diastolic, self.hypertension]:
            if _ < 0:
                raise ValueError(F'{_} must be a positive integer')

        for _ in [self.weight, self.fat, self.pulse, self.temperature]:
            if _ < 0:
                raise ValueError(F'{_} must be a positive real number.')

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
        record = F'{A.now().format("YYYY-MM-DD HH:mm")},{self.po_pulse},{self.spox},{self.weight},{self.fat},{self.pulse},{self.systolic},{self.diastolic},{self.ihb},{self.hypertension},{self.temperature}'
        with DATA_FILE.open('a',encoding='utf-8') as data_file:
            hr_data = data_file.write(F"{record}\n")
            logging.info("Recorded: %s", record)
            return hr_data
