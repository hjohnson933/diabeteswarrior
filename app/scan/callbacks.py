# from datetime import datetime as dt

import hashlib
from pathlib import Path as P
from shutil import copyfile as Cpf

import arrow as Arw
from dash.dependencies import Input, Output
from flask_login import current_user

from .config import BASE_FILE_NAME, DATA_FILE_HEADER, DATA_ROOT


def scan_setup(data_file, backup_file):
    data_file = P(data_file)
    backup_file = P(backup_file)

    if not data_file.exists():
        data_file.touch(mode=0o666, exist_ok=True)
        with data_file.open('a', encoding='utf-8') as new_data_file:
            new_data_file.write(F'{DATA_FILE_HEADER}\n')

    if not backup_file.exists():
        backup_file.touch(mode=0o666, exist_ok=True)


def archived_status(data_file, backup_file) -> bool:
    df_hash = hashlib.sha256(data_file.read_bytes()).hexdigest()
    bf_hash = hashlib.sha256(backup_file.read_bytes()).hexdigest()
    return df_hash == bf_hash


def backup_restore(opcode, data_file, backup_file) -> str:
    if archived_status(data_file, backup_file):
        return 'The data file is already archived.'
    if opcode == 'c':
        Cpf(data_file, backup_file)
        return 'The data file was successfully archived.'
    if opcode == 'd':
        Cpf(backup_file, data_file)
        return 'The data file was restored successfully.'
    return 'Opecode must be "c" or "d".'


def register_callbacks(dashapp):
    # @dashapp.callback(
    #     Output('my-graph', 'figure'),
    #     Input('data-scope', 'value'),
    #     State('user-store', 'data')
    # )
    # def update_graph(selected_dropdown_value, data) -> dict:
    #     df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
    #     return {'data': [{'x': df.index, 'y': df.Close}], 'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}}

    @dashapp.callback(
        Output('user-store', 'data'),
        Input('scope-dropdown-menu', 'value')
    )
    def cur_user(children) -> str:
        if current_user.is_authenticated:
            DATA_FILE = F'{DATA_ROOT}/{current_user.username}_{BASE_FILE_NAME}.csv'
            BACKUP_FILE = F'{DATA_FILE}.backup'
            scan_setup(DATA_FILE, BACKUP_FILE)
            return {
                'username': current_user.username,
                'data_file': DATA_FILE,
                'backup_file': BACKUP_FILE
            }

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
        Output('button-feedback', 'children'),
        Output('submit-button', 'disabled'),
        Input('submit-button', 'n_clicks'),
        Input('glucose-input', 'value'),
        Input('user-store', 'data')
    )
    def submit_restore_backup(submit_button, glucose_input, user_store):
        """Disable submit button till there is a glucose value entered.
        Disable the restore and backup buttons if the data and backup files are the same."""

        if glucose_input is None:
            submit_enabled = 'disabled'
        else:
            submit_enabled = None

        return str(user_store), submit_enabled
