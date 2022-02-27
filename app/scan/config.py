from pathlib import Path as Pth

MODULE_ROOT = Pth(__file__).parent

DATA_ROOT = MODULE_ROOT.joinpath('data')

BASE_FILE_NAME = 'scan'

DATA_FILE_HEADER = ["ts", "message", "notes", "bolus", "bolus_u", "basal", "basal_u", "food", "carbohydrate", "exercise", "medication", "glucose", "trend", "lower_limit", "upper_limit"]

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

BTN_DICT = {
    'scope': ['Last 24 hours', 'Last 14 days', 'Last 90 days'],
    'event': ['No Special Event', 'Bolus Insulin', 'Basal Insulin', 'Meal', 'Medication', 'Execrise'],
    'message': ['Is high', 'Is going high', 'My high alarm', 'No alarm', 'My low alarm', 'Is going low', 'Is low'],
    'trend': ['Pointing up', 'Pointing up and right', 'Pointing right', 'Pointing down and right', 'Pointing down']
    }
