# import statistics
# import json

import flask
import pandas as pd
from app import BaseConfig
from dash import Input, Output

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

    rv = pd.read_sql_query(F'SELECT DISTINCT foods.index, foods.ts, users.username, foods.domain, foods.name, foods.portion, units.v, foods.calories, foods.fat, foods.cholesterol, foods.sodium, foods.carbohydrate, foods.protein FROM foods LEFT JOIN users on foods.user_id = users.id LEFT JOIN units on foods.unit = units.k WHERE foods.user_id = {uid} ORDER BY foods.index', conn, index_col='index')
    return rv


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('datatable-interactivity', 'data'),
        Output('datatable-interactivity', 'columns'),
        Output('datatable-interactivity', 'filter_action'),
        Output('intermediate-value', 'data'),
        Input('datatable-interactivity', 'derived_virtual_selected_rows')
    )
    def update_output(derived_virtual_selected_rows):
        dff = ''
        uid = flask.request.cookies['userID']
        df = make_data_frame(uid)

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

        if derived_virtual_selected_rows is not None and len(derived_virtual_selected_rows) > 0:
            df = df.iloc[derived_virtual_selected_rows]
            dff = df.to_json()

        return data, columns, filter_action, dff

    @dashapp.callback(
        Output('servings', 'children'),
        Input('intermediate-value', 'data')
    )
    def update_table(data):
        label = []
        if len(data) != 0:
            df = pd.read_json(data)
            label.append(df[['domain', 'name']])

        print(label)
        # todo build meal form

        return 'data'
