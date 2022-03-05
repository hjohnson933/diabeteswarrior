"""Scan Dash Application Callbacks"""

import arrow
import dash
from dash.dependencies import Input, Output
from flask_login import current_user

from .assets.utils import max_idx, write_db

scope_dict = {'Last 24 hours': 24, 'Last 14 days': 336, 'Last 90 days': 2160}
message_dict = {'Is high': 3, 'Is going high': 2, 'My high alarm': 1, 'No alarm': 0, 'My low alarm': -1, 'Is going low': -2, 'Is low': -3}
trend_dict = {'Pointing up': 2, 'Pointing up and right': 1, 'Pointing right': 0, 'Pointing down and right': -1, 'Pointing down': -2}


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('user-store', 'data'),
        Input('scope-scan-menu', 'value')
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
        Output('submit-scan-button', 'n_clicks'),
        Output('event-scan-menu', 'value'),
        Output('message-scan-menu', 'value'),
        Output('trend-scan-menu', 'value'),
        Output('glucose-scan-input', 'value'),
        Output('bolus_unit-scan-input', 'value'),
        Output('basal_unit-scan-input', 'value'),
        Output('carbohydrate-scan-input', 'value'),
        Output('notes-scan-input', 'value'),
        Output('timetamp-scan-input', 'value'),
        Input('event-scan-menu', 'value'),
        Input('message-scan-menu', 'value'),
        Input('trend-scan-menu', 'value'),
        Input('glucose-scan-input', 'value'),
        Input('bolus_unit-scan-input', 'value'),
        Input('basal_unit-scan-input', 'value'),
        Input('carbohydrate-scan-input', 'value'),
        Input('notes-scan-input', 'value'),
        Input('timetamp-scan-input', 'value'),
        Input('submit-scan-button', 'n_clicks')
    )
    def submit_record(event, message, trend, glucose, bolus_u, basal_u, carbohydrate, notes, timestamp, submit_button):
        ctx = dash.callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        bolus = False
        basal = False
        food = False
        medication = False
        exercise = False
        lower_limit = -1
        upper_limit = 1
        trend_n = trend_dict[trend]
        index = max_idx(table='scan')

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

        scan = {
            'index': [index + 1],
            'ts': [arrow.now().format("YYYY-MM-DD HH:mm")],
            'message': [message_dict[message]],
            'notes': [notes],
            'glucose': [glucose],
            'trend': [trend_n],
            'bolus': [bolus],
            'bolus_u': [bolus_u],
            'basal': [basal],
            'basal_u': [basal_u],
            'food': [food],
            'carbohydrate': [carbohydrate],
            'medication': [medication],
            'exercise': [exercise],
            'lower_limit': [lower_limit],
            'upper_limit': [upper_limit]
        }

        if button_id == 'submit-scan-button' and glucose is not None and submit_button > 0:
            write_db(records=scan, table='scan')
            return 0, 'No Special Event', 'No alarm', 'Pointing right', None, None, None, None, '', arrow.now().format("YYYY-MM-DD HH:mm")
        else:
            return submit_button, event, message, trend, glucose, bolus_u, basal_u, carbohydrate, notes, arrow.now().format("YYYY-MM-DD HH:mm")

    # @dashapp.callback(
    #     Output('my-graph', 'figure'),
    #     Input('data-scope', 'value'),
    #     State('user-store', 'data')
    # )
    # def update_graph(selected_scan_value, data) -> dict:
    #     df = pdr.get_data_yahoo(selected_scan_value, start=dt(2017, 1, 1), end=dt.now())
    #     return {'data': [{'x': df.index, 'y': df.Close}], 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}}
