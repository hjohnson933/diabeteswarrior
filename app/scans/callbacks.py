import arrow
import flask
import pandas as pd
from app import BaseConfig
from app.models import Scans, Users, Messages, Trends, Targets
from dash import Input, Output, dash_table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

conn = BaseConfig.SQLALCHEMY_DATABASE_URI


def total_insulin(bolus: int, basal: int) -> int:
    """"Calculates the total insulin

        Parameters:
        ----------
        bolus : int
            Foreground insulin
        basal : int
            Background insulin

        Returns : int
            Total insulin dose
    """

    return bolus + basal


def make_data_frame(uid) -> object:
    """ Makes the dictionary of data and returns a pandas data frame

        Parameters
        ----------
            uid : int
                Id of the logged in user

        Returns : object
            Pandas data frame

    """

    engine = create_engine(conn)
    Session = sessionmaker(bind=engine)
    session = Session()

    results = session.query(Scans, Users, Messages, Trends, Targets).\
        filter(Scans.user_id == Users.id).\
        filter(Scans.user_id == Targets.user_id).\
        filter(Scans.message == Messages.k).\
        filter(Scans.trend == Trends.k).\
        filter(Users.id == uid).\
        all()

    result_dict = {}
    for result in results:
        insulin = 0
        carbohydrate = 0
        medication = 'No'
        exercise = 'No'

        if result[0].bolus or result[0].basal:
            insulin = total_insulin(result[0].bolus_u, result[0].basal_u)
        if result[0].food:
            carbohydrate = result[0].carbohydrate
        if result[0].medication:
            medication = "Yes"
        if result[0].exercise:
            exercise = "Yes"

        result_dict[result[0].index] = {
            'when': arrow.get(result[0].ts, 'US/Central').humanize(),
            'username': result[1].username,
            'alert': result[2].v,
            'notes': result[0].notes,
            'glucose': result[0].glucose,
            'trend': result[3].v,
            'insulin': insulin,
            'carbohydrate': carbohydrate,
            'medication': medication,
            'exercise': exercise,
            'trend_lower': result[0].lower_limit,
            'trend_upper': result[0].upper_limit,
            'chart_lower': result[4].chart_min,
            'chart_upper': result[4].chart_max,
            'limit_lower': result[4].limit_min,
            'limit_upper': result[4].limit_max,
            'target_lower': result[4].target_min,
            'target_upper': result[4].target_max,
            'my_target_lower': result[4].my_target_min,
            'my_target_upper': result[4].my_target_max,
            'my_target_weight': result[4].my_target_weight,
            'my_target_bmi': result[4].my_target_bmi,
            'meal_ideal': result[4].meal_ideal,
            'meal_good': result[4].meal_good,
            'meal_bad': result[4].meal_bad
        }

    return pd.DataFrame.from_dict(result_dict, 'index')


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
                {'name': 'alert', 'id': 'alert'},
                {'name': 'notes', 'id': 'notes'},
                {'name': 'glucose', 'id': 'glucose'},
                {'name': 'trend', 'id': 'trend'},
                {'name': 'insulin', 'id': 'insulin'},
                {'name': 'carbohydrate', 'id': 'carbohydrate'},
                {'name': 'medication', 'id': 'medication'},
                {'name': 'exercise', 'id': 'exercise'}
            ],
            filter_action='native',
            page_action='native',
            sort_action='native',
            # page_current=0,
            # page_size=15,
            style_cell={'backgroundColor': 'black', 'font-size': '12px'}
        )

        return rv
