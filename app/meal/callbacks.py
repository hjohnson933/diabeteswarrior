"""Meal Dash Application Callbacks"""

# import arrow
import dash
# import pandas as pd
from dash.dependencies import Input, Output
from flask_login import current_user

# from .assets.utils import write_db

scope_dict = {'Last 24 hours': 24, 'Last 14 days': 336, 'Last 90 days': 2160}


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('user-store', 'data'),
        Input('scope-meal-menu', 'value')
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
            return F"Interface for User: {data['username']}"

    @dashapp.callback(
        Output('test-output', 'children'),
        Input('food-table', 'derived_virtual_data'),
        Input('food-table', 'derived_virtual_selected_rows'),
        Input('submit-meal-button', 'n_clicks'),
        Input('submit-food-button', 'n_clicks'),
        Input('calc-meal-button', 'n_clicks')
    )
    def calc_meal(dvd, dvsr, smmb, sffb, cmfb) -> str:
        """ dvsr is the index of the selected food item from the table.
            dvd is a indexed list of dictionaries containing the data for the selected food items."""
        ctx = dash.callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        indices = ''
        # ? submit-meal-button
        # ? submit-food-button
        if button_id == 'calc-meal-button':
            for each in dvsr:
                indices += F"{each};"
                indices = indices.strip()
            if indices.endswith(';'):
                indices = indices.rstrip(';')

        return indices
