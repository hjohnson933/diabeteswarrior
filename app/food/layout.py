from dash import dcc, html

layout = html.Div(id='main', children=[
    html.H1(id='username'),
    dcc.Dropdown(id='my-dropdown', options=[{'label': 'Food', 'value': 'food'}, {'label': 'Meal', 'value': 'meal'}]),
    dcc.Store(id='user-store')
])
