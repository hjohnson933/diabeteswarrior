from dataclasses import dataclass


@dataclass
class ScanRecords:
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
            raise ValueError("Glucose must be a positive integer.")

    def record_add(self, DATA_FILE) -> int:
        with DATA_FILE.open('a', encoding='utf-8') as data:
            hr_data = data.write(f'{self.ts},{self.message},"{self.notes}",{self.bolus},{self.bolus_u},{self.basal},{self.basal_u},{self.food},{self.carbohydrate},{self.exercise},{self.medication},{self.glucose},{self.trend},{self.lower_limit},{self.upper_limit}\n')
        return hr_data
