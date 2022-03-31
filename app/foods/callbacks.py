import json

from collections import deque
from dataclasses import dataclass  # , asdict
# from datetime import datetime
from typing import NamedTuple

import flask
import pandas as pd
from app import BaseConfig
from dash import Input, Output, dcc, html
from dash.exceptions import PreventUpdate

conn = BaseConfig.SQLALCHEMY_DATABASE_URI


@dataclass
class Item(NamedTuple):
    """ A subset of the FoodItem table that is displayed in the meal form.

    Parameters:
    -----------
        index : int
            The pandas dataframe index.
        domain : str
            The kitchen, chef, cook, manufacture or distributor of the food item.
        name : str
            The name of the food item.
        servings : int
            The number of servings you plan on or had of this food item.
    """

    index: int
    domain: str
    name: str
    servings: float


def make_foods_data_frame(uid) -> object:
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


def make_children(child: tuple, r: int, v: bool = False) -> list[str]:
    """Returns a list of html elements for the servings table.

    Arguments:
    ---------
        item : tuple
            A tuple of Item namedtuples.
        r : int
            The row number.
    """

    children = []

    if v:
        children.append(
            html.Div(
                id=F"index_{r}",
                className="form-group col-1",
                children=[
                    dcc.Input(
                        id=F"index_{r}_input_{child.Index}",
                        value=child.Index,
                    )
                ]
            ),
        )

        children.append(
            html.Div(
                id=F"domain_{r}",
                className="form-group col-3",
                children=[
                    dcc.Input(
                        id=F"domain_{r}_input_{child.Index}",
                        value=child.domain,
                    )
                ]
            ),
        )

        children.append(
            html.Div(
                id=F"name_{r}",
                className="form-group col-6",
                children=[
                    dcc.Input(
                        id=F"name_{r}_input_{child.Index}",
                        value=child.name,
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
                        id=F"servings_{r}_input_{child.Index}",
                        type="text",
                        size="5",
                        value=child.servings,
                    )
                ]
            ),
        )

    else:
        children.append(
            html.Div(
                id=F"index_{r}",
                className="form-group col-1",
                children=[
                    dcc.Input(
                        id=F"index_{r}_input_{child.Index}",
                        placeholder=child.Index,
                    )
                ]
            ),
        )

        children.append(
            html.Div(
                id=F"domain_{r}",
                className="form-group col-3",
                children=[
                    dcc.Input(
                        id=F"domain_{r}_input_{child.Index}",
                        placeholder=child.domain,
                    )
                ]
            ),
        )

        children.append(
            html.Div(
                id=F"name_{r}",
                className="form-group col-6",
                children=[
                    dcc.Input(
                        id=F"name_{r}_input_{child.Index}",
                        placeholder=child.name,
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
                        id=F"servings_{r}_input_{child.Index}",
                        type="text",
                        size="5",
                        placeholder=child.servings,
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
        df = make_foods_data_frame(uid)

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
            dff = dff.assign(servings=0.0).to_json()

        return data, columns, filter_action, dff

    @dashapp.callback(
        Output('meals-table', 'columns'),
        Output('meals-table', 'data'),
        Input('filtered_foods', 'data'),
        Input('servings_input', 'value'),
        Input('foods_table', 'derived_virtual_selected_rows')
    )
    def process_servings_form(filtered_foods, servings_input, derived_virtual_selected_rows):
        """Display the domain and name for each selected food item in the Meal form. While the servings value is
        None or 0 wait for the user to enter a value then multiply the other values in for the selected food items and
        accumulate the totals in the meals table. When all food items have been entered with servings values and the
        meal submit button is clicked, the meal is added to the database the form is rest.

        Arguments:
        ---------
            filtered_foods str:
                The Domain, Name and Servings for each selected food item.
            servings_input float:
                The number of servings for the selected food item in decimal.
            derived_virtual_selected_rows list[int]:
                A list of integers representing the selected rows in the Foods table.
        """

        # print(type(derived_virtual_selected_rows[0]))
        indices = {s for s in derived_virtual_selected_rows}

        columns = [
            {'name': 'calories', 'id': 'calories'},
            {'name': 'fat', 'id': 'fat'},
            {'name': 'cholesterol', 'id': 'cholesterol'},
            {'name': 'sodium', 'id': 'sodium'},
            {'name': 'carbohydrate', 'id': 'carbohydrate'},
            {'name': 'protein', 'id': 'protein'},
            {'name': 'serving', 'id': 'serving'},
            {'name': 'indexes', 'id': 'indexes'}
        ]

        data = {
            'calories': 0.0,
            'fat': 0.0,
            'cholesterol': 0.0,
            'sodium': 0.0,
            'carbohydrate': 0.0,
            'protein': 0.0,
            'serving': "",
            'indexes': str(indices)
        }

        try:
            d = json.loads(filtered_foods)
        except json.decoder.JSONDecodeError:
            ...

        try:
            print(d['servings'])
        except UnboundLocalError:
            ...

        # get the indexes in the derived_virtual_selected_rows and add them to the indices set
        # indices.add(derived_virtual_selected_rows)

    #     items = deque()

    #     # * if the user has selected a row, add the row to the items deque
    #     if len(filtered_foods) > 0:
    #         df = pd.read_json(filtered_foods)
    #         dfs = df[['domain', 'name', 'servings']]
    #         items.extend(dfs.itertuples(index=True, name='Item'))

    #     print(len(items))
    #     while items:
    #         print('While')
    #         indices.add(items[0].Index)
    #         items.popleft()
    #     else:
    #         print('else')
    #         print(indices)
    #     # while items:
    #     #     print(items)
    #         # if items[0].Index not in indices:
    #         #     indices.add(items[0].Index)
    #         # else:
    #         #     items.popleft()

    #     # * In this callback, we process each item and add it to the accumulator
    #     # for r, child in enumerate(items):
    #     #     serving_each_item.append(
    #     #         html.Div(id=F"row_{r}", className="form-group m-2 row", children=make_children(child, r),)
    #     #     )

    #     meals_dict = {
    #         'calories': [0.0],
    #         'fat': [0.0],
    #         'cholesterol': [0.0],
    #         'sodium': [0.0],
    #         'carbohydrate': [0.0],
    #         'protein': [0.0],
    #         'serving': [""],
    #         'indexes': [str(indices)],
    #     }
    #     meals_df = pd.DataFrame(meals_dict)
    #     data = meals_df.to_dict('records')

    #     # print(indices)
    #     # print(items)

        return columns, [data]
