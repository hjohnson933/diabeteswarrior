import flask
import pandas as pd
from app import BaseConfig
from dash import Input, Output, dash_table

conn = BaseConfig.SQLALCHEMY_DATABASE_URI


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('table-contents', 'children'),
        Input('table-contents', 'children')
    )
    def update_output(children):
        uid = flask.request.cookies['userID']
        df = pd.read_sql(F'SELECT * FROM scans WHERE user_id = {uid}', conn)
        rv = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            filter_action='native',
            page_action='native',
            page_current=0,
            page_size=25
        )

        return rv
