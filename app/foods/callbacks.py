# import statistics
# import json

import flask
import pandas as pd
from app import BaseConfig
from dash import Input, Output, html, dcc

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

    rv = pd.read_sql_query(
        F'SELECT DISTINCT foods.index, foods.ts, users.username, foods.domain, foods.name, foods.portion, units.v, foods.calories, foods.fat, foods.cholesterol, foods.sodium, foods.carbohydrate, foods.protein FROM foods LEFT JOIN users on foods.user_id = users.id LEFT JOIN units on foods.unit = units.k WHERE foods.user_id = {uid} ORDER BY foods.index', conn, index_col='index')
    return rv


def make_meal_form() -> object:
    rv = html.Form(
        id="meal_form",
        title="Food Item Servings",
        children=[
            html.Fieldset(
                id="meal_fieldset",
                form="meal_form",
                children=[
                    html.Legend(
                        id="meal_fieldset_legend",
                        children=["Meal"]
                    ),
                    html.Label(
                        id="domain_label",
                        form="meal_form",
                        htmlFor="domain_input",
                        children=["Domain:"]
                    ),
                    dcc.Input(
                        id="domain_input",
                        type="text",
                        value="domain",
                        readOnly=True
                    ),
                    html.Label(
                        id="name__label",
                        form="meal_form",
                        htmlFor="name_input",
                        children=["Name:"]
                    ),
                    dcc.Input(
                        id="name_input",
                        type="text",
                        value="name",
                        readOnly=True
                    ),
                    html.Label(
                        id="servings_label",
                        form="meal_form",
                        htmlFor="servings_input",
                        children=["Servings:"]
                    ),
                    dcc.Input(
                        id="servings_input",
                        type="number",
                        value="servings",
                    )
                ]),
            html.Button()
        ]
    )

    return rv


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('foods_table', 'data'),
        Output('foods_table', 'columns'),
        Output('foods_table', 'filter_action'),
        Output('filtered_foods', 'data'),
        Input('foods_table', 'derived_virtual_selected_rows')
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
            filtered_indexes = df.index
            dff = df.loc[filtered_indexes]
            dff = dff.assign(servings=1.0).to_json()

        return data, columns, filter_action, dff

    @dashapp.callback(
        Output('servings_table', 'children'),
        Input('filtered_foods', 'data'),
        # Input('servings_table', 'derived_virtual_data'),
    )
    def update_table(filtered_foods):
        servings = make_meal_form()

        try:
            # df = pd.read_json(filtered_foods)
            return servings
        except ValueError:
            ...

        return servings
