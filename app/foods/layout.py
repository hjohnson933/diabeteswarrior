from dash import dcc, html, dash_table

layout = html.Div(id="food-main", className="container-fluid", children=[
    html.Div(id='servings_table'),
    # dash_table.DataTable(
    #     id='servings_table',
    #     style_cell={'backgroundColor': 'black', 'font-size': '11px'},
    #     columns=[
    #         # {'name': 'index', 'id': 'index'},
    #         {'name': 'domain', 'id': 'domain'},
    #         {'name': 'name', 'id': 'name'},
    #         {'name': 'servings', 'id': 'servings'}
    #     ],
    #     page_current=0,
    #     page_size=6,
    #     editable=True
    # ),
    html.Br(),
    dash_table.DataTable(
        id='foods_table',
        style_cell={'backgroundColor': 'black', 'font-size': '11px', 'textAlign': 'left'},
        style_data={'whitespace': 'normal', 'height': 'auto', 'lineHeight': '15px'},
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
