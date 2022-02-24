"""Interface to the model"""
from dataclasses import dataclass

import arrow as Arw
from .utils import FOOD_DATA_FILE, MEAL_DATA_FILE


@dataclass
class FoodRecords:
    ts: str
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

    def __post_init__(self) -> None:
        self.domain = self.domain.replace(',', ';')
        self.name = self.name.replace(',', ';')
        self.portion = self.portion.replace(',', ';')
        self.unit = self.unit.replace(',', ';')
        self.calories = int(self.calories)
        self.fat = int(self.fat)
        self.cholesterol = int(self.cholesterol)
        self.sodium = int(self.sodium)
        self.carbohydrate = int(self.carbohydrate)
        self.protein = int(self.protein)

    def __repr__(self) -> str:
        return f'Food: {self.ts},{self.domain},{self.name},{self.portion},{self.unit},{self.calories},{self.fat},{self.cholesterol},{self.sodium},{self.carbohydrate},{self.protein}'

    def record_add(self) -> int:
        with FOOD_DATA_FILE.open("a") as data_file:
            hr_data = data_file.write(f'{Arw.now().format("YYYY-MM-DD HH:mm")},"{self.domain}","{self.name}","{self.portion}","{self.unit}",{self.calories},{self.fat},{self.cholesterol},{self.sodium},{self.carbohydrate},{self.protein}\n')
        return hr_data


@dataclass
class MealRecords:
    ts: str
    calories: int
    fat: int
    sodium: int
    carbohydrate: int
    protein: int
    servings: list[float]
    indices: list[float]

    def __post_init__(self) -> None:
        self.calories = int(self.calories)
        self.fat = int(self.fat)
        self.cholesterol = int(self.cholesterol)
        self.sodium = int(self.sodium)
        self.carbohydrate = int(self.carbohydrate)
        self.protein = int(self.protein)

    def __repr__(self):
        return f'Meal: {self.ts}, {self.calories}, {self.fat}, {self.sodium}, {self.carbohydrate}, {self.protein}, "{self.servings}", "{self.indices}"'

    def record_add(self) -> int:
        with MEAL_DATA_FILE.open("a") as data_file:
            hr_data = data_file.write(F'{Arw.now().format("YYYY-MM-DD HH:mm")}, {self.calories}, {self.fat}, {self.sodium}, {self.carbohydrate}, {self.protein}, "{self.servings}", "{self.indices}"\n')
        return hr_data
