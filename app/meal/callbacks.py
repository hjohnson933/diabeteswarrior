"""Meal Dash Application Callbacks"""

import arrow
import dash

from dash.dependencies import Input, Output
from flask_login import current_user

from .assets.utils import max_idx, write_db

scope_dict = {'Last 24 hours': 24, 'Last 14 days': 336, 'Last 90 days': 2160}


def register_callbacks(dashapp):
    @dashapp.callback(Output('user-store', 'data'),
        Input('scope-meal-menu', 'value'))
    def cur_user(children) -> str:
        if current_user.is_authenticated:
            name = {'username': current_user.username}
            return name
        return ''

    @dashapp.callback(Output('username', 'children'),
        Input('user-store', 'data'))
    def username(data) -> str:
        if data is None:
            return ''
        else:
            return F"Interface for User: {data['username']}"

    @dashapp.callback(Output('test-output', 'children'),
        Output('calories-meal-input', 'value'),
        Output('fat-meal-input', 'value'),
        Output('cholesterol-meal-input', 'value'),
        Output('sodium-meal-input', 'value'),
        Output('carbohydrate-meal-input', 'value'),
        Output('protein-meal-input', 'value'),
        Output('servings-meal-input', 'value'),
        Output('indices-meal-input', 'value'),
        Output('submit-meal-button', 'n_clicks'),
        Input('food-table', 'derived_virtual_data'),
        Input('food-table', 'derived_virtual_selected_rows'),
        Input('calories-meal-input', 'value'),
        Input('fat-meal-input', 'value'),
        Input('cholesterol-meal-input', 'value'),
        Input('sodium-meal-input', 'value'),
        Input('carbohydrate-meal-input', 'value'),
        Input('protein-meal-input', 'value'),
        Input('submit-meal-button', 'n_clicks'))
    def calc_meal(dvd, dvsr, calories, fat, cholesterol, sodium, carbohydrate, protein, smb):
        ctx = dash.callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        calories = 0
        fat = 0
        cholesterol = 0
        sodium = 0
        carbohydrate = 0
        protein = 0
        servings = []
        indices = []

        if dvsr is not None:
            for each in dvsr:
                each_serving = float(dvd[each]['serving'])
                calories += dvd[each]['calories'] * each_serving
                fat += dvd[each]['fat'] * each_serving
                cholesterol += dvd[each]['cholesterol'] * each_serving
                sodium += dvd[each]['sodium'] * each_serving
                carbohydrate += dvd[each]['carbohydrate'] * each_serving
                protein += dvd[each]['protein'] * each_serving
                servings.append(dvd[each]['serving'])
                indices.append(dvd[each]['index'])

        servings = str(servings).replace(', ', ';').replace('[', '').replace(']', '').replace("'", "")
        indices = str(indices).replace(', ', ';').replace('[', '').replace(']', '').replace("'", "")

        if button_id == 'submit-meal-button' and smb > 0:
            meal = {
                'index': [max_idx('meal') + 1],
                'ts': [arrow.now().format("YYYY-MM-DD HH:mm")],
                'calories': [calories],
                'fat': [fat],
                'cholesterol': [cholesterol],
                'sodium': [sodium],
                'carbohydrate': [carbohydrate],
                'protein': [protein],
                'servings': [servings],
                'indices': [indices]
            }
            write_db(meal, 'meal')
            dvsr = []
            return button_id, 0, 0, 0, 0, 0, 0, '', '', 0

        return button_id, calories, fat, cholesterol, sodium, carbohydrate, protein, servings, indices, smb
