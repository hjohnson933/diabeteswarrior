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


def make_children(items, r=0) -> list:
    children = []

    for i, j in enumerate(items):
        # ? https://github.com/plotly/dash-core-components/pull/185
        # * for now a bug in Dash core components prevents the use of the  disabled and readOnly attributes
        # if j[2]:
        #     read_req = 'readonly'
        # else:
        #     read_req = 'required'
        children.append(
            html.Div(
                id=F"row_{r}_col_{i}",
                className="form-group col-2",
                children=[
                    html.Label(
                        form="form-control-label",
                        htmlFor=F"{j[0]}_input",
                        children=[F"{j[0].capitalize()}:"]
                    ),
                    dcc.Input(
                        # read_req,
                        id=F"servings_{j[0]}_input",
                        type=F"{j[1]}",
                        value=j[3]
                    ),
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
        # Input('servings_table', 'derived_virtual_data'),
    )
    def update_table(filtered_foods):
        items = [('domain', 'text', True, 'domain'), ('name', 'text', True, 'name'), ('servings', 'number', False, 1.0)]

        servings = []
        servings.append(dcc.Input(id="csrf_token", name="csrf_token", type="hidden", value="test_secret_key"),)
        servings.append(html.Legend(id="servings_fieldset_legend", className="border-bottom mb-4", children=["Meal"]),)
        # start the loop here
        for r in range(1):
            servings.append(
                html.Div(
                    id=F"row_{r}",
                    className="form-group m-2 row",
                    children=make_children(items)
                ),
            )

        # if len(filtered_foods) != 0:
        #     df = pd.read_json(filtered_foods)

        # try:
        #     return make_field_set(zip(df.index, df['domain'], df['name'], df['servings']))
        # except UnboundLocalError:
        #     ...

        return servings
