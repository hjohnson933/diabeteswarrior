from dash.dependencies import Input, Output, State
from flask_login import current_user


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('user-store', 'data'),
        Input('my-dropdown', 'value'),
        State('user-store', 'data')
        )
    def cur_user(args, data):
        if current_user.is_authenticated:
            return current_user.username

    @dashapp.callback(Output('username', 'children'), Input('user-store', 'data'))
    def username(data):
        if data is None:
            return ''
        else:
            return f'Hello {data}'
