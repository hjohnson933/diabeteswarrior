from dash import dcc, html, dash_table

layout = html.Div(id="food-main", className="container-fluid", children=[
    html.Div(
        id="meal-accumulator",
        className="row",
        children="Meal Accumulator"
    ),
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
                form="servings_form"
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
