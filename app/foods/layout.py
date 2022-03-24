from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

layout = html.Div(id="food-main", className="container-fluid", children=[
    dbc.Form(
        id='servings',
        children=[
            dbc.Col(id="servings-description", children=[]),
            dbc.Col(id="servings-input", children=[])
        ]
    ),
    html.Br(),
    dash_table.DataTable(
        id='datatable-interactivity',
        style_cell={'backgroundColor': 'black', 'font-size': '11px'},
        page_current=0,
        page_size=10,
        editable=True,
        row_selectable='multi',
        selected_rows=[],
        selected_cells=[],
        page_action='native',
        sort_action='native',
        cell_selectable=True
    ),
    dcc.Store(id='intermediate-value')
])
