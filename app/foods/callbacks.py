# import statistics
import json

import arrow
import flask
import pandas as pd
from app import BaseConfig
from app.models import Foods, Units, Users
from dash import Input, Output
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

conn = BaseConfig.SQLALCHEMY_DATABASE_URI


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
    results = session.query(Foods, Users, Units).\
        filter(Foods.unit == Units.k).\
        filter(Foods.user_id == Users.id).\
        filter(Users.id == uid).order_by(Foods.index).all()

    result_dict = {}
    for result in results:
        result_dict[result[0].index] = {
            'when': arrow.get(result[0].ts, 'US/Central').humanize(),
            'username': result[1].username,
            'domain': result[0].domain,
            'name': result[0].name,
            'portion': result[0].portion,
            'unit': result[2].v,
            'calories': result[0].calories,
            'fat': result[0].fat,
            'cholesterol': result[0].cholesterol,
            'sodium': result[0].sodium,
            'carbohydrate': result[0].carbohydrate,
            'protein': result[0].protein
        }

    rv = pd.DataFrame.from_dict(result_dict, 'index')
    return rv


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('datatable-interactivity', 'data'),
        Output('datatable-interactivity', 'columns'),
        Output('datatable-interactivity', 'filter_action'),
        Output('intermediate-value', 'data'),
        Input('datatable-interactivity', 'derived_virtual_selected_rows'),
        Input('datatable-interactivity', 'derived_virtual_data')
    )
    def update_output(derived_virtual_selected_rows, derived_virtual_data):
        jd = []
        odff = ''
        uid = flask.request.cookies['userID']
        df = make_data_frame(uid)
        dvd = derived_virtual_data

        data = df.to_dict('records')
        columns = [{'name': 'domain', 'id': 'domain'},
                   {'name': 'name', 'id': 'name'},
                   {'name': 'portion', 'id': 'portion'},
                   {'name': 'unit', 'id': 'unit'},
                   {'name': 'calories', 'id': 'calories'},
                   {'name': 'fat', 'id': 'fat'},
                   {'name': 'cholesterol', 'id': 'cholesterol'},
                   {'name': 'sodium', 'id': 'sodium'},
                   {'name': 'carbohydrate', 'id': 'carbohydrate'},
                   {'name': 'protein', 'id': 'protein'}]
        filter_action = 'native'

        # ? Postprocessing
        for each in derived_virtual_selected_rows:
            jd.append(json.dumps(dvd[each]))

        dff = pd.DataFrame(jd)
        if dff.empty:
            ...
        else:
            odff = dff.to_json()
        return data, columns, filter_action, odff

    @dashapp.callback(
        Output('table', 'children'),
        Input('intermediate-value', 'data')
    )
    def update_table(data):
        do = ''
        if len(data) == 0:
            ...
        else:
            do = pd.read_json(data)
        print(do)
        return data
