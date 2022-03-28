from dataclasses import dataclass
from typing import NamedTuple

import flask
import pandas as pd
from app import BaseConfig
from dash import Input, Output, dcc, html

conn = BaseConfig.SQLALCHEMY_DATABASE_URI


@dataclass
class Item(NamedTuple):
    domain: str
    name: str
    servings: float


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
        F'SELECT DISTINCT foods.index, foods.ts, users.username, foods.domain, foods.name, foods.portion, foods.unit, foods.calories, foods.fat, foods.cholesterol, foods.sodium, foods.carbohydrate, foods.protein FROM foods LEFT JOIN users on foods.user_id = users.id LEFT JOIN units on foods.unit = units.k WHERE foods.user_id = {uid} ORDER BY foods.index', conn, index_col='index')
    return rv


def make_children(items, r) -> list:
    children = []
    children.append(
        html.Div(
            id=F"domain_{r}",
            className="form-group col-5",
            children=[
                dcc.Input(
                    id=F"domain_{r}_input",
                    value=items[r].domain,
                )
            ]
        ),
    )
    children.append(
        html.Div(
            id=F"name_{r}",
            className="form-group col-5",
            children=[
                dcc.Input(
                    id=F"name_{r}_input",
                    value=items[r].name,
                )
            ]
        ),
    )
    children.append(
        html.Div(
            id=F"servings_{r}",
            className="form-group col-2",
            children=[
                dcc.Input(
                    id=F"servings_{r}_input",
                    type="text",
                    size="5",
                    value=items[r].servings,
                )
            ]
        ),
    )

    return children


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
        Output('servings_fieldset', 'children'),
        Input('filtered_foods', 'data'),
        # todo Input('servings_table', 'derived_virtual_data'),
    )
    def update_table(filtered_foods):
        item_count = 0

        items = []
        item = NamedTuple('Item', [('domain', str), ('name', str), ('servings', float)])
        items.append(item(domain='Domain', name='Name', servings=1.0))

        if len(filtered_foods) > 0:
            items = []
            df = pd.read_json(filtered_foods)
            item_count = df.shape[0]
            dfs = df[['domain', 'name', 'servings']]
            for row in dfs.itertuples(index=False):
                items.append(row)

        servings = []
        servings.append(dcc.Input(id="csrf_token", name="csrf_token", type="hidden", value="test_secret_key"),)
        servings.append(html.Legend(id="servings_fieldset_legend", className="border-bottom mb-4", children=["Meal"]),)
        servings.append(html.Div(id="label_row", className="form-group m-2 row", children=[
            html.Div(className="form-control-label col-5", children=["Domain:"]),
            html.Div(className="form-control-label col-5", children=["Name:"]),
            html.Div(className="form-control-label col-2", children=["Servings:"]),
        ]),)

        for r in range(item_count):
            servings.append(
                html.Div(
                    id=F"row_{r}",
                    className="form-group m-2 row",
                    children=make_children(items, r)
                ),
            )

        return servings
