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

    @dashapp.callback(
        Output('submit-button', 'n_clicks'),
        Output('event-dropdown-menu', 'value'),
        Output('message-dropdown-menu', 'value'),
        Output('trend-dropdown-menu', 'value'),
        Output('glucose-input', 'value'),
        Output('bolus_unit-input', 'value'),
        Output('basal_unit-input', 'value'),
        Output('carbohydrate-input', 'value'),
        Output('notes-input', 'value'),
        Output('timetamp-input', 'value'),
        Input('event-dropdown-menu', 'value'),
        Input('message-dropdown-menu', 'value'),
        Input('trend-dropdown-menu', 'value'),
        Input('glucose-input', 'value'),
        Input('bolus_unit-input', 'value'),
        Input('basal_unit-input', 'value'),
        Input('carbohydrate-input', 'value'),
        Input('notes-input', 'value'),
        Input('timetamp-input', 'value'),
        Input('submit-button', 'n_clicks')
    )
    def submit_scan_record(event, message, trend, glucose, bolus_u, basal_u, carbohydrate, notes, timestamp, submit_button):
        """Hold session data till the submit button is pressed. It then writes the data to the database and reset the form. If the submint button is pressed before you have valid glucose data then session is held until the blood sugar data is entered. Blood glucose level is the only required data."""

        ctx = dash.callback_context

        bolus = False
        basal = False
        food = False
        medication = False
        exercise = False
        lower_limit = -1
        upper_limit = 1
        trend_n = trend_dict[trend]
        index = 0
        with Engine.begin() as connection:
            index = pd.read_sql_table('scan', connection)['index'].count()

        if trend_n == -2:
            lower_limit = -12
            upper_limit = -2
        elif trend_n == -1:
            lower_limit = -2
            upper_limit = -1
        elif trend_n == 1:
            lower_limit = 1
            upper_limit = 2
        elif trend_n == 2:
            lower_limit = 2
            upper_limit = 12

        if bolus_u is not None:
            bolus = True

        if basal_u is not None:
            basal = True

        if carbohydrate is not None:
            food = True

        if event == 'Medication':
            medication = True

        if event == 'Execrise':
            exercise = True

        scan = {'index': [index + 1], 'ts': [arrow.now().format("YYYY-MM-DD HH:mm")], 'message': [message_dict[message]], 'notes': [notes], 'glucose': [glucose], 'trend': [trend_n], 'bolus': [bolus], 'bolus_u': [bolus_u], 'basal': [basal], 'basal_u': [basal_u], 'food': [food], 'carbohydrate': [carbohydrate], 'medication': [medication], 'exercise': [exercise], 'lower_limit': [lower_limit], 'upper_limit': [upper_limit]}
        df = pd.DataFrame(data=scan)
        df.set_index('index')

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'submit-button' and glucose is not None and submit_button > 0:
            with Engine.begin() as connection:
                df.to_sql('scan', con=connection, if_exists='append')
            return 0, 'No Special Event', 'No alarm', 'Pointing right', None, None, None, None, '', arrow.now().format("YYYY-MM-DD HH:mm")
        else:
            return submit_button, event, message, trend, glucose, bolus_u, basal_u, carbohydrate, notes, arrow.now().format("YYYY-MM-DD HH:mm")

    # @dashapp.callback(
    #     Output('my-graph', 'figure'),
    #     Input('data-scope', 'value'),
    #     State('user-store', 'data')
    # )
    # def update_graph(selected_dropdown_value, data) -> dict:
    #     df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
    #     return {'data': [{'x': df.index, 'y': df.Close}], 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}}
