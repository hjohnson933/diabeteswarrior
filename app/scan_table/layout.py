from dash import html

layout = html.Div(
    className="container-fluid",
    children=[
        html.A(
            id="nav-to-home",
            style={'font-size': '175%'},
            href="/home/",
            children="Diabetes Warrior"
        ),
        html.Div(id="table-contents")
    ])
