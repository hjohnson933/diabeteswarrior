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
            name = {'username': current_user.username}
            return str(name)
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
        Input('event-dropdown-menu', 'value'),
        Input('message-dropdown-menu', 'value'),
        Input('trend-dropdown-menu', 'value'),
        Input('glucose-input', 'value'),
        Input('bolus_unit-input', 'value'),
        Input('basal_unit-input', 'value'),
        Input('carbohydrate-input', 'value'),
        Input('notes-input', 'value'),
        Input('submit-button', 'n_clicks')
    )
    def submit_scan_record(event, message, trend, glucose, bolus_u, basal_u, carbohydrate, notes, submit_button):
        """Hold session data till the submit button is pressed. It then writes the data to the database and reset the form. If the submint button is pressed before you have valid glucose data then session is held until the blood sugar data is entered. Blood glucose level is the only required data."""

        session = Session()
        ctx = dash.callback_context

        bolus = False
        basal = False
        food = False
        medication = False
        exercise = False
        lower_limit = -1
        upper_limit = 1
        trend_n = trend_dict[trend]

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

        scan = Records(
            ts=Arw.now().format("YYYY-MM-DD HH:mm"),
            message=message_dict[message],
            notes=notes,
            glucose=glucose,
            trend=trend_n,
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

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'submit-button' and glucose is not None:
            session.add(scan)
            if submit_button > 0:
                session.commit()
                return 0, 'No Special Event', 'No alarm', 'Pointing right', None, None, None, None, None
        else:
            return submit_button, event, message, trend, glucose, bolus_u, basal_u, carbohydrate, notes

    # @dashapp.callback(
    #     Output('my-graph', 'figure'),
    #     Input('data-scope', 'value'),
    #     State('user-store', 'data')
    # )
    # def update_graph(selected_dropdown_value, data) -> dict:
    #     df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
    #     return {'data': [{'x': df.index, 'y': df.Close}], 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}}
