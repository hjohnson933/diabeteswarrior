"""Dash Application Callbacks"""

import arrow
import dash
import pandas as pd
from dash.dependencies import Input, Output
from flask_login import current_user

from .ifaces import Engine

scope_dict = {'Last 24 hours': 24, 'Last 14 days': 336, 'Last 90 days': 2160}
stage_dict = {'No Hypertension': 0, 'Pre-Hypertension': 1, 'Stage I Hypertension': 2, 'Stage II Hypertension': 3}
ihb_dict = {'Regular Heart Beat': 0, 'Irregular Heart Beat': 1}


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
        Output('timetamp-input', 'value'),
        Output('po_pulse-input', 'value'),
        Output('po_ox-input', 'value'),
        Output('weight-input', 'value'),
        Output('fat-input', 'value'),
        Output('bpc_pulse-input', 'value'),
        Output('bpc_systolic-input', 'value'),
        Output('bpc_diastolic-input', 'value'),
        Output('ihb-dropdown-menu', 'value'),
        Output('stage-dropdown-menu', 'value'),
        Output('temperature-input', 'value'),
        Input('temperature-input', 'value'),
        Input('stage-dropdown-menu', 'value'),
        Input('ihb-dropdown-menu', 'value'),
        Input('bpc_diastolic-input', 'value'),
        Input('bpc_systolic-input', 'value'),
        Input('bpc_pulse-input', 'value'),
        Input('fat-input', 'value'),
        Input('weight-input', 'value'),
        Input('po_ox-input', 'value'),
        Input('po_pulse-input', 'value'),
        Input('timetamp-input', 'value'),
        Input('submit-button', 'n_clicks')
    )
    def submit_record(temperature, stage, bpc_ihb, bpc_diastolic, bpc_systolic, bpc_pulse, fat, weight, po_ox, po_pulse, timestamp, submit_button):
        ctx = dash.callback_context
        form_valid = False
        timestamp = arrow.now().format("YYYY-MM-DD HH:MM")
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        index = 0
        with Engine.begin() as connection:
            index = pd.read_sql('health', connection)['index'].count()

        if po_pulse is not None and po_pulse > 0 and po_ox is not None and po_ox > 0 and weight is not None and weight > 0 \
            and fat is not None and fat > 0 and bpc_pulse is not None and bpc_pulse > 0 and bpc_systolic is not None and \
                bpc_systolic > 0 and bpc_diastolic is not None and bpc_diastolic > 0 and temperature is not None and temperature > 0:
            form_valid = True

        if form_valid and button_id == 'submit-button' and submit_button > 0:
            health = {'index': [index + 1], 'ts': timestamp, 'po_pulse': po_pulse, 'po_ox': po_ox, 'weight': weight, 'fat': fat, 'bpc_pulse': bpc_pulse, 'bpc_systolic': bpc_systolic, 'bpc_diastolic': bpc_diastolic, 'bpc_hypertension': stage_dict[stage], 'bpc_ihb': ihb_dict[bpc_ihb], 'temperature': temperature}
            print(health)
            return 0, timestamp, None, None, None, None, None, None, None, 'Regular Heart Beat', 'No Hypertension', None

        return submit_button, timestamp, po_pulse, po_ox, weight, fat, bpc_pulse, bpc_systolic, bpc_diastolic, bpc_ihb, stage, temperature

    # @dashapp.callback(
    #     Output('my-graph', 'figure'),
    #     Input('data-scope', 'value'),
    #     State('user-store', 'data')
    # )
    # def update_graph(selected_dropdown_value, data) -> dict:
    #     df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
    #     return {'data': [{'x': df.index, 'y': df.Close}], 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}}
