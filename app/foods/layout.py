from dash import dcc, html, dash_table

layout = html.Div(id="food-main", className="container-fluid", children=[
    html.Div(
        id="food-header-0",
        className="row",
        children=[]
    ),
    html.Div(
        id="food-header-1",
        children=[]
    ),
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
    dcc.Store(id='filtered_foods'),
    dcc.Store(id='indexed_servings')
])
