import json

from collections import deque
from dataclasses import dataclass  # , asdict
# from datetime import datetime
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


def make_children(child: tuple) -> list[str]:
    """Returns a list of html elements for the servings table.

    Arguments:
    ---------
        item : tuple
            A tuple of Item namedtuples.
    """

    children = []

    children.append(
        html.Div(
            id="data_row_index",
            className="form-group col-1",
            children=[
                dcc.Input(
                    id="index_input",
                    placeholder=child.Index,
                )
            ]
        ),
    )

    children.append(
        html.Div(
            id="data_row_domain",
            className="form-group col-3",
            children=[
                dcc.Input(
                    id="domain_input",
                    placeholder=child.domain,
                )
            ]
        ),
    )

    children.append(
        html.Div(
            id="data_row_name_{r}",
            className="form-group col-6",
            children=[
                dcc.Input(
                    id="name_input",
                    placeholder=child.name,
                )
            ]
        ),
    )

    children.append(
        html.Div(
            id="data_row_servings",
            className="form-group col-2",
            children=[
                dcc.Input(
                    id="servings_input",
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
    def make_filter_store_food_data(derived_virtual_selected_rows):
        """_summary_

        Args:
            derived_virtual_selected_rows (_type_): _description_

        Returns:
            _type_: _description_
        """        
        filtered_foods_df = ''
        login_user_id = flask.request.cookies['userID']
        all_foods_df = make_foods_data_frame(login_user_id)

        data = all_foods_df.to_dict('records')
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
            all_foods_df = all_foods_df.iloc[derived_virtual_selected_rows]
            filtered_indexes = all_foods_df.index
            filtered_foods_df = all_foods_df.loc[filtered_indexes]
            filtered_foods_df = filtered_foods_df.assign(servings=0.0).to_json()

        return data, columns, filter_action, filtered_foods_df

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

        indices = {s for s in derived_virtual_selected_rows}
        items = deque()
        servings = deque()
        # meals_table_data = deque()

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
            'serving': str(servings),
            'indexes': str(indices)
        }

        # Now add each of the filtered foods to the items deque
        try:
            d = json.loads(filtered_foods)
            filtered_foods_df = pd.DataFrame(d)
            data_row_df = filtered_foods_df[['domain', 'name', 'servings']]
            items.extend(data_row_df.itertuples(index=True))

            data = {
                k: v for k, v in (
                    ('calories', filtered_foods_df.calories.cumsum().values[0]),
                    ('fat', filtered_foods_df.fat.cumsum().values[0]),
                    ('cholesterol', filtered_foods_df.cholesterol.cumsum().values[0]),
                    ('sodium', filtered_foods_df.sodium.cumsum().values[0]),
                    ('carbohydrate', filtered_foods_df.carbohydrate.cumsum().values[0]),
                    ('protein', filtered_foods_df.protein.cumsum().values[0]),
                    # ('serving', filtered_foods_df.serving.cumsum().values[0]),
                    # ('indexes', filtered_foods_df.indexes.cumsum().values[0])
                )
            }
            # print(data)
        except json.decoder.JSONDecodeError:
            ...

        if len(items) > 0:
            item = items.popleft()
            print(item.Index)
            print(item.domain)
            print(item.name)
            print(item.servings)

        return columns, [data]
