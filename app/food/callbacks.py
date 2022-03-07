"""Meal Dash Application Callbacks"""

import arrow
import dash
from dash.dependencies import Input, Output
from flask_login import current_user
from .assets.utils import max_idx, write_db, nav_home

scope_dict = {'Last 24 hours': 24, 'Last 14 days': 336, 'Last 90 days': 2160}


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('user-store', 'data'),
        Input('scope-food-menu', 'value')
    )
    def cur_user(children) -> str:
        if current_user.is_authenticated:
            name = {'username': current_user.username}
            return name
        return ''

    @dashapp.callback(
        Output('username', 'children'),
        Input('user-store', 'data')
    )
    def username(data) -> str:
        if data is None:
            return ''
        else:
            return nav_home(data['username'])

    @dashapp.callback(Output('submit-food-button', 'n_clicks'),
        Output('timetamp-food-input', 'value'),
        Output('domain-food-input', 'value'),
        Output('name-food-input', 'value'),
        Output('portion-food-input', 'value'),
        Output('unit-food-menu', 'value'),
        Output('calories-food-input', 'value'),
        Output('fat-food-input', 'value'),
        Output('cholesterol-food-input', 'value'),
        Output('sodium-food-input', 'value'),
        Output('carbohydrate-food-input', 'value'),
        Output('protein-food-input', 'value'),
        Input('submit-food-button', 'n_clicks'),
        Input('timetamp-food-input', 'value'),
        Input('domain-food-input', 'value'),
        Input('name-food-input', 'value'),
        Input('portion-food-input', 'value'),
        Input('unit-food-menu', 'value'),
        Input('calories-food-input', 'value'),
        Input('fat-food-input', 'value'),
        Input('cholesterol-food-input', 'value'),
        Input('sodium-food-input', 'value'),
        Input('carbohydrate-food-input', 'value'),
        Input('protein-food-input', 'value'))
    def new_food(sfb, timestamp, domain, name, portion, unit, calories, fat, cholesterol, sodium, carbohydrate, protein) -> str:
        ctx = dash.callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        index = max_idx(table='food')
        food = {
            'index': [index + 1]
        }

        if domain is not None and name is not None and calories is not None and fat is not None and cholesterol is not None and sodium is not None and carbohydrate is not None and protein is not None:
            food['ts'] = [arrow.now().format("YYYY-MM-DD HH:mm")]
            food['domain'] = [domain]
            food['name'] = [name]
            food['portion'] = [portion]
            food['unit'] = [unit]
            food['calories'] = [calories]
            food['fat'] = [fat]
            food['cholesterol'] = [cholesterol]
            food['sodium'] = sodium
            food['carbohydrate'] = [carbohydrate]
            food['protein'] = [protein]

        if button_id == 'submit-food-button' and sfb > 0:
            write_db(records=food, table='food')
            sfb = 0
            timestamp = arrow.now().format("YYYY-MM-DD HH:mm")
            domain = name = portion = ''
            unit = 'g'
            calories = fat = cholesterol = sodium = carbohydrate = protein = protein = None
            return sfb, timestamp, domain, name, portion, unit, calories, fat, cholesterol, sodium, carbohydrate, protein

        return sfb, timestamp, domain, name, portion, unit, calories, fat, cholesterol, sodium, carbohydrate, protein
