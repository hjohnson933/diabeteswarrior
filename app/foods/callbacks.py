import json

from collections import deque
from dataclasses import dataclass  # , asdict
# from datetime import datetime
from typing import NamedTuple

import flask
import pandas as pd
from app import BaseConfig
from dash import Input, Output

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


def register_callbacks(dashapp):
    @dashapp.callback(
        Output('foods_table', 'data'),
        Output('foods_table', 'columns'),
        Output('foods_table', 'filter_action'),
        Output('filtered_foods', 'data'),
        Input('foods_table', 'derived_virtual_selected_rows')
    )
    def get_filter_store_food_data(derived_virtual_selected_rows):
        """Get the logged in user's id and retrive the foods from the database as a pandas dataframe.
        Convert the dataframe to a dictionary and send it to the foods_table so it can be selected for the
        current meal. The selected food items are stored in the `filtered_foods` store for use in the next
        callback.

        Arguments:
        ----------
            derived_virtual_selected_rows dict:
                The user selected rows from the foods_table.

        Returns:
            tuple:
                food_table_data:
                    pandas data frame as a dictionary
                food_table_columns:
                    column names of the food table
                filter_action:
                    type of filter the table uses, it should be noted that most of the table formattind and
                    controls are set in the `layout.py` file.
                filtered_foods_data:
                    selected rows from the foods_table as a dictionary.
        """

        filtered_foods_df = ''
        login_user_id = flask.request.cookies['userID']
        all_foods_df = make_foods_data_frame(login_user_id)

        food_table_data = all_foods_df.to_dict('records')
        food_table_columns = [{'name': 'domain', 'id': 'domain'},
                   {'name': 'name', 'id': 'name'},
                   {'name': 'portion', 'id': 'portion'},
                   {'name': 'unit', 'id': 'unit'},
                   {'name': 'calories', 'id': 'calories'},
                   {'name': 'fat', 'id': 'fat'},
                   {'name': 'cholesterol', 'id': 'cholesterol'},
                   {'name': 'sodium', 'id': 'sodium'},
                   {'name': 'carbohydrate', 'id': 'carbohydrate'},
                   {'name': 'protein', 'id': 'protein'}]
        food_table_filter_action = 'native'

        if derived_virtual_selected_rows is not None and len(derived_virtual_selected_rows) > 0:
            all_foods_df = all_foods_df.iloc[derived_virtual_selected_rows]
            filtered_indexes = all_foods_df.index
            filtered_foods_df = all_foods_df.loc[filtered_indexes]
            filtered_foods_df = filtered_foods_df.assign(servings=0.0).to_json()

        return food_table_data, food_table_columns, food_table_filter_action, filtered_foods_df

    @dashapp.callback(
        Output('indexed_servings', 'data'),
        Output('index_input', 'value'),
        Output('domain_input', 'value'),
        Output('name_input', 'value'),
        Output('servings_input', 'value'),
        Input('filtered_foods', 'data'),
        Input('servings_input', 'value'),
        Input('foods_table', 'derived_virtual_selected_rows')
    )
    def set_food_item_servings(filtered_foods, servings_input, derived_virtual_selected_rows):
        """
        """

        data = {}
        items = deque()
        index_input = None
        domain_input = None
        name_input = None
        servings_input = None

        try:
            records_list = set()

            filtered_foods_data = json.loads(filtered_foods)
            filtered_foods_df = pd.DataFrame(filtered_foods_data)
            records = filtered_foods_df[['domain', 'name', 'servings']].to_dict('index')
            for k, v in records.items():
                records_list.add((int(k) - 1, (v['domain'], v['name'], v['servings'])))
            items.extend(records_list)
        except json.decoder.JSONDecodeError:
            ...

        try:
            print(items)
        except IndexError:
            ...

        # for item in items:
        #     index_input, value = item
        #     domain_input, name_input, servings_input = value

        return data, index_input, domain_input, name_input, servings_input
