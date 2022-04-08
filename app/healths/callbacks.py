import statistics

import arrow
import flask
import pandas as pd
from app import BaseConfig
from app.models import Healths, Hypert, Targets, Users
from dash import Input, Output, dash_table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

conn = BaseConfig.SQLALCHEMY_DATABASE_URI


def avg_pulse(po_pulse: int, bpc_pulse: int) -> int:
    pulse = [po_pulse, bpc_pulse]
    return round(statistics.mean(pulse))


def make_data_frame(uid) -> object:
    """ Makes the dictionary of data and returns a pandas data frame

        Parameters
        ----------
            uid : int
                Id of the logged in user

        Returns : object
            Pandas data frame

    """

    result_dict = {}
    engine = create_engine(conn)
    Session = sessionmaker(bind=engine)
    session = Session()

    results = session.query(Healths, Users, Hypert, Targets).\
        filter(Healths.user_id == Users.id).\
        filter(Healths.bpc_hypertension == Hypert.k).\
        filter(Healths.user_id == Targets.user_id).\
        filter(Users.id == uid).\
        all()

    for result in results:
        ihb = 'Regular'
        if result[0].bpc_ihb:
            ihb = 'Irregular'
        result_dict[result[0].index] = {
            'when': arrow.get(result[0].ts, 'US/Central').humanize(),
            'username': result[1].username,
            'temperature': result[0].temperature,
            'pulse': avg_pulse(result[0].po_pulse, result[0].bpc_pulse),
            'oxygen': result[0].po_ox,
            'systolic': result[0].bpc_systolic,
            'diastolic': result[0].bpc_diastolic,
            'heart': ihb,
            'hypertension': result[2].v,
            'weight': result[0].weight,
            'target_weight': float(result[3].my_target_weight),
            'bmi': result[0].fat,
            'target_bmi': float(result[3].my_target_bmi)
        }

    rv = pd.DataFrame.from_dict(result_dict, 'index')
    return rv


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('table-contents', 'children'),
        Input('table-contents', 'children')
    )
    def update_output(children):
        uid = flask.request.cookies['userID']
        df = make_data_frame(uid)

        rv = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[
                {'name': 'when', 'id': 'when'},
                {'name': 'temperature', 'id': 'temperature'},
                {'name': 'pulse', 'id': 'pulse'},
                {'name': 'oxygen', 'id': 'oxygen'},
                {'name': 'systolic', 'id': 'systolic'},
                {'name': 'diastolic', 'id': 'diastolic'},
                {'name': 'heart', 'id': 'heart'},
                {'name': 'hypertension', 'id': 'hypertension'},
                {'name': 'weight', 'id': 'weight'},
                {'name': 'bmi', 'id': 'bmi'}
            ],
            filter_action='native',
            page_action='native',
            sort_action='native',
            # page_current=0,
            # page_size=15,
            style_cell={'backgroundColor': 'black', 'font-size': '12px'}
        )

        return rv
