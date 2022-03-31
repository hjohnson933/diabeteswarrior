from dash import dcc, html, dash_table

layout = html.Div(id="food-main", className="container-fluid", children=[
    dash_table.DataTable(
        id="meals-table",
        style_table={'width': '100%'},
        style_cell={
            'backgroundColor': 'black',
            'textAlign': 'left',
            'font-size': '11px',
            'maxWidth': '0',
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px',
        },
    ),
    html.Br(),
    html.Div(
        id="food-header-0",
        className="row",
        children=[]
    ),
    html.Div(
        id="food-header-1",
        className="row",
        children=[]
    ),
    html.Form(
        id="servings_form",
        title="Food Item Servings",
        children=[
            html.Fieldset(
                id="servings_fieldset",
                className="form-group",
                form="servings_form",
                children=[
                    dcc.Input(
                        id="csrf_token",
                        name="csrf_token",
                        type="hidden",
                        value="test_secret_key"
                    ),
                    html.Legend(
                        id="servings_fieldset_legend",
                        className="border-bottom mb-4",
                        children=["Meal"]
                    ),
                    html.Div(
                        id="label_row",
                        className="form-group m-2 row",
                        children=[
                            html.Div(className="form-control-label col-1", children=["Index: "]),
                            html.Div(className="form-control-label col-3", children=["Domain:"]),
                            html.Div(className="form-control-label col-6", children=["Name:"]),
                            html.Div(className="form-control-label col-2", children=["Servings:"]),
                        ]
                    ),
                    html.Div(
                        id="data_row",
                        className="form-group m-2 row",
                        children=[
                            html.Div(
                                id="data_row_index",
                                className="form-group col-1",
                                children=[
                                    dcc.Input(
                                        id="index_input",
                                        placeholder=0,
                                    )
                                ]
                            ),
                            html.Div(
                                id="data_row_domain",
                                className="form-group col-3",
                                children=[
                                    dcc.Input(
                                        id="domain_input",
                                        placeholder="Domian",
                                    )
                                ]
                            ),
                            html.Div(
                                id="data_row_name",
                                className="form-group col-6",
                                children=[
                                    dcc.Input(
                                        id="name_input",
                                        placeholder="Name",
                                    )
                                ]
                            ),
                            html.Div(
                                id="data_row_servings",
                                className="form-group col-2",
                                children=[
                                    dcc.Input(
                                        id="servings_input",
                                        type="number",
                                        size="5",
                                        placeholder="Servings"
                                    )
                                ]
                            ),
                        ],
                    )
                ]
            ),
            html.Button(
                id="meal_submit_button",
                title="Meal Submit Button",
                name="meal_submit_button",
                className="form-group btn btn-outline-info",
                form="servings_form",
                children="Meal Submit"
            )
        ]
    ),
    html.Br(),
    dash_table.DataTable(
        id='foods_table',
        style_table={'width': '100%'},
        fixed_rows={'headers': True, 'data': 0},
        style_cell={
            'backgroundColor': 'black',
            'textAlign': 'left',
            'font-size': '11px',
            'maxWidth': '0',
        },
        style_cell_conditional=[
            {'if': {'column_id': 'domain'}, 'width': '15%'},
            {'if': {'column_id': 'name'}, 'width': '35%'},
        ],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px',
        },
        editable=True,
        row_selectable='multi',
        selected_rows=[],
        selected_cells=[],
        page_action='native',
        sort_action='native',
        cell_selectable=True
    ),
    dcc.Store(id='filtered_foods')
])
