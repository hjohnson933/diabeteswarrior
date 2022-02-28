import json

import arrow as Arw
import dash
from dash.dependencies import Input, Output
from flask_login import current_user
from sqlalchemy.orm import sessionmaker

from .ifaces import Engine, Records

scope_dict = {'Last 24 hours': 24, 'Last 14 days': 336, 'Last 90 days': 2160}
message_dict = {'Is high': 3, 'Is going high': 2, 'My high alarm': 1, 'No alarm': 0, 'My low alarm': -1, 'Is going low': -2, 'Is low': -3}
trend_dict = {'Pointing up': 2, 'Pointing up and right': 1, 'Pointing right': 0, 'Pointing down and right': -1, 'Pointing down': -2}

Session = sessionmaker()
Session.configure(bind=Engine)


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('user-store', 'data'),
        Input('scope-dropdown-menu', 'value')
    )
    def cur_user(children) -> str:
        if current_user.is_authenticated:
            return {'username': current_user.username}

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
        Output('confirm-scan-output', 'children'),
        Input('user-store', 'data'),
        Input('message-dropdown-menu', 'value'),
        Input('trend-dropdown-menu', 'value'),
        Input('glucose-input', 'value'),
        Input('bolus_unit-input', 'value'),
        Input('basal_unit-input', 'value'),
        Input('carbohydrate-input', 'value'),
        Input('event-dropdown-menu', 'value'),
        Input('notes-input', 'value'),
        Input('submit-button', 'n_clicks'),
        Input('confirm-scan-input', 'submit_n_clicks')
    )
    def submit_restore_backup(user_store, message, trend, glucose, bolus_u, basal_u, carbohydrate, event, notes, submit_button, confirm):
        """Disable submit button till there is a glucose value entered.
        Disable the restore and backup buttons if the data and backup files are the same."""

        session = Session()
        ctx = dash.callback_context

        bolus = False
        basal = False
        food = False
        medication = False
        exercise = False
        lower_limit = -1
        upper_limit = 1
        trend = trend_dict[trend]

        if trend == -2:
            lower_limit = -12
            upper_limit = -2
        elif trend == -1:
            lower_limit = -2
            upper_limit = -1
        elif trend == 1:
            lower_limit = 1
            upper_limit = 2
        elif trend == 2:
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

        scan = Records(
            ts=Arw.now().format("YYYY-MM-DD HH:mm"),
            message=message_dict[message],
            notes=notes,
            glucose=glucose,
            trend=trend,
            bolus=bolus,
            bolus_u=bolus_u,
            basal=basal,
            basal_u=basal_u,
            food=food,
            carbohydrate=carbohydrate,
            medication=medication,
            exercise=exercise,
            lower_limit=lower_limit,
            upper_limit=upper_limit
            )

        
        # session.add(scan)
        # print(session.commit())
        return "Test"

    # @dashapp.callback(
    #     Output('my-graph', 'figure'),
    #     Input('data-scope', 'value'),
    #     State('user-store', 'data')
    # )
    # def update_graph(selected_dropdown_value, data) -> dict:
    #     df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
    #     return {'data': [{'x': df.index, 'y': df.Close}], 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}}
