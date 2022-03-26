from dataclasses import dataclass

import flask
import pandas as pd
from app import BaseConfig
from dash import Input, Output, dcc, html

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


@dataclass
class Meal:
    index: int = 0
    domain: str = "This field is populated when a food item is selected."
    name: str = "This field is populated when a food item is selected."
    servings: int = 1


def make_field_set(field_set_data: object) -> list[object]:
    # field_set_items = list(field_set_data)
    children = [
        dcc.Input(id="csrf_token", name="csrf_token", type="hidden", value="test_secret_key"),
        html.Legend(id="servings_fieldset_legend", className="border-bottom mb-4", children=["Meal"]),
        # ? loop through the data and create a fieldset for each item
        # todo move the html.Div into the __str__ of the dataclass Meal
        html.Div(
            id="row_0",
            className="form-group m-2 row",
            children=[
                html.Div(
                    id="row_0_col_0",
                    className="form-group col-2",
                    children=[ html.Label( form="form-control-label", htmlFor="index_input", children=["Index:"] ), dcc.Input( id="servings_index_input", type="number", value="index", readOnly=True ), ]
                ),
                html.Div(
                    id="row_0_col_1",
                    className="form-group col-2",
                    children=[ html.Label( form="servings_form", htmlFor="domain_input", children=["Domain:"] ), dcc.Input( id="servings_domain_input", type="text", value="domain", readOnly=True ), ]
                ),
                html.Div(
                    id="row_0_col_2",
                    className="form-group col-2",
                    children=[ html.Label( id="servings_name_label", form="servings_form", htmlFor="name_input", children=["Name:"] ), dcc.Input( id="servings_name_input", type="text", value="name", readOnly=True ) ]
                ),
                html.Div(
                    id="row_0_col_3",
                    className="form-group col-2",
                    children=[ html.Label( id="servings_serving_label", form="servings_form", htmlFor="servings_input", children=["Servings:"] ), dcc.Input( id="servings_serving_input", type="number", value="servings" ) ]
                )
            ]
        ),
    ]

    # for item in field_set_items:
    #     print(item)

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
        # Input('servings_table', 'derived_virtual_data'),
    )
    def update_table(filtered_foods):
        servings = []
        servings.append(dcc.Input(id="csrf_token", name="csrf_token", type="hidden", value="test_secret_key"),)
        servings.append(html.Legend(id="servings_fieldset_legend", className="border-bottom mb-4", children=["Meal"]),)
        # start the loop here
        servings.append(
            html.Div(
                id="row_0",
                className="form-group m-2 row",
                children=[
                    html.Div(
                        id="row_0_col_0",
                        className="form-group col-2",
                        children=[
                            html.Label(
                                form="form-control-label",
                                htmlFor="index_input",
                                children=["Index:"]
                            ),
                            dcc.Input(
                                id="servings_index_input",
                                type="number",
                                value="index",
                                readOnly=True
                            ),
                        ]
                    ),
                    html.Div(
                        id="row_0_col_1",
                        className="form-group col-2",
                        children=[
                            html.Label(
                                form="servings_form",
                                htmlFor="domain_input",
                                children=["Domain:"]
                            ),
                            dcc.Input(
                                id="servings_domain_input",
                                type="text",
                                value="domain",
                                readOnly=True
                            ),
                        ]
                    ),
                    html.Div(
                        id="row_0_col_2",
                        className="form-group col-2",
                        children=[
                            html.Label(
                                id="servings_name_label",
                                form="servings_form",
                                htmlFor="name_input",
                                children=["Name:"]
                            ),
                            dcc.Input(
                                id="servings_name_input",
                                type="text",
                                value="name",
                                readOnly=True
                            )
                        ]
                    ),
                    html.Div(
                        id="row_0_col_3",
                        className="form-group col-2",
                        children=[
                            html.Label(
                                id="servings_serving_label",
                                form="servings_form",
                                htmlFor="servings_input",
                                children=["Servings:"]
                            ),
                            dcc.Input(
                                id="servings_serving_input",
                                type="number",
                                value="servings"
                            )
                        ]
                    )
                ]
            ),
        )

        # if len(filtered_foods) != 0:
        #     df = pd.read_json(filtered_foods)

        # try:
        #     return make_field_set(zip(df.index, df['domain'], df['name'], df['servings']))
        # except UnboundLocalError:
        #     ...

        return servings
