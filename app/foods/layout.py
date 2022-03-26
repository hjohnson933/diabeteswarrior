from dash import dcc, html, dash_table

layout = html.Div(id="food-main", className="container-fluid", children=[
    html.Form(
        id="servings_form",
        title="Food Item Servings",
        children=[
            html.Fieldset(
                id="servings_fieldset",
                form="servings_form",
                children=[
                    html.Legend(id="servings_fieldset_legend", children=["Meal"]),
                    html.Label(id="servings_index_label", form="servings_form", htmlFor="index_input", children=["Index:"]),
                    dcc.Input(id="servings_index_input", type="number", value="index", readOnly=True),
                    html.Label(id="servings_domain_label", form="servings_form", htmlFor="domain_input", children=["Domain:"]),
                    dcc.Input(id="servings_domain_input", type="text", value="domain", readOnly=True),
                    html.Label(id="servings_name_label", form="servings_form", htmlFor="name_input", children=["Name:"]),
                    dcc.Input(id="servings_name_input", type="text", value="name", readOnly=True),
                    html.Label(id="servings_serving_label", form="servings_form", htmlFor="servings_input", children=["Servings:"]),
                    dcc.Input(id="servings_serving_input", type="number", value="servings")
                ]),
            html.Button()
        ]
    ),
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
    dcc.Store(id='filtered_foods'),
    html.Div(id="null")
])
