"""Meal Dash Application Callbacks"""

import arrow
import dash
import pandas as pd
from dash.dependencies import Input, Output
from flask_login import current_user

from .assets.utils import Engine

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

    # @dashapp.callback(
    #     Output('my-graph', 'figure'),
    #     Input('data-scope', 'value'),
    #     State('user-store', 'data')
    # )
    # def update_graph(selected_dropdown_value, data) -> dict:
    #     df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
    #     return {'data': [{'x': df.index, 'y': df.Close}], 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}}
