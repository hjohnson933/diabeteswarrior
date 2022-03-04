"""Dash Application Callbacks"""

import arrow
import dash
import pandas as pd
from dash.dependencies import Input, Output
from flask_login import current_user

from .ifaces import Engine

scope_dict = {'Last 24 hours': 24, 'Last 14 days': 336, 'Last 90 days': 2160}
message_dict = {'Is high': 3, 'Is going high': 2, 'My high alarm': 1, 'No alarm': 0, 'My low alarm': -1, 'Is going low': -2, 'Is low': -3}
trend_dict = {'Pointing up': 2, 'Pointing up and right': 1, 'Pointing right': 0, 'Pointing down and right': -1, 'Pointing down': -2}


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('user-store', 'data'),
        Input('scope-dropdown-menu', 'value')
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
