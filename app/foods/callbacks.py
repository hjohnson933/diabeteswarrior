from collections import deque
from dataclasses import dataclass
from typing import NamedTuple

import flask
import pandas as pd
from app import BaseConfig
from dash import Input, Output, dcc, html


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


def make_children(child: tuple, r: int) -> list[str]:
    """Returns a list of html elements for the servings table.

    Arguments:
    ---------
        item : tuple
            A tuple of Item namedtuples.
        r : int
            The row number.
    """

    children = []

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
    )
    def update_table(filtered_foods) -> list[str]:
        serving_each_item = []
        items = []

        # * create the default item
        item = NamedTuple('Item', [('Index', int), ('domain', str), ('name', str), ('servings', float)])
        items.append(item(Index=0, domain='Domain', name='Name', servings=0.0))

        # * Start building the servings entry form by adding a hidden field setting the legend and displaying the header row.
        serving_each_item.append(dcc.Input(id="csrf_token", name="csrf_token", type="hidden", value="test_secret_key"),)
        serving_each_item.append(html.Legend(id="servings_fieldset_legend", className="border-bottom mb-4", children=["Meal"]),)
        serving_each_item.append(html.Div(id="label_row", className="form-group m-2 row", children=[
            html.Div(className="form-control-label col-1", children=["Index: "]),
            html.Div(className="form-control-label col-3", children=["Domain:"]),
            html.Div(className="form-control-label col-6", children=["Name:"]),
            html.Div(className="form-control-label col-2", children=["Servings:"]),
        ]),)

        # * In this callback, we just add the default item to the page
        for r, child in enumerate(items):
            serving_each_item.append(
                html.Div(id=F"row_{r}", className="form-group m-2 row", children=make_children(child, r),)
            )

        return serving_each_item

    @dashapp.callback(
        Output('meal-accumulator', 'children'),
        Input('filtered_foods', 'data'),
    )
    def process_servings_form(filtered_foods):
        items = deque()
        indices = set()

        # * if the user has selected a row, add the row to the items deque
        if len(filtered_foods) > 0:
            df = pd.read_json(filtered_foods)
            dfs = df[['domain', 'name', 'servings']]
            items.extend(dfs.itertuples(index=True, name='Item'))

        # * In this callback, we process each item and add it to the accumulator
        # for r, child in enumerate(items):
        #     serving_each_item.append(
        #         html.Div(id=F"row_{r}", className="form-group m-2 row", children=make_children(child, r),)
        #     )

        print(indices)
        print(items)
        while items:
            if items[0].Index not in indices:
                indices.add(items[0].Index)
            else:
                items.popleft()
        print(indices)
        print(items)
        ...
