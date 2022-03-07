"""Meal Dash Application Layout"""
import arrow
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table

from .assets.utils import dropdown_input, form_buttons, user_input, get_table_data

BTN_DICT = {
    'scope': ['Last 24 hours', 'Last 14 days', 'Last 90 days'],
    'unit': [{'label': 'Cup', 'value': 'c'},
             {'label': 'Fluid ounce', 'value': 'fl oz'},
             {'label': 'Gallon', 'value': 'gal'},
             {'label': 'Milliliter', 'value': 'ml'},
             {'label': 'Liter', 'value': 'l'},
             {'label': 'Pint', 'value': 'pt'},
             {'label': 'Quart', 'value': 'qt'},
             {'label': 'Tablespoon', 'value': 'tbsp'},
             {'label': 'Teaspoon', 'value': 'tsp'},
             {'label': 'Gram', 'value': 'g'},
             {'label': 'Kilogram', 'value': 'kg'},
             {'label': 'Pound', 'value': 'lb'},
             {'label': 'Milligram', 'value': 'mg'},
             {'label': 'Ounce', 'value': 'oz'},
             {'label': 'Dozen', 'value': 'doz'},
             {'label': 'Large', 'value': 'lg'},
             {'label': 'Pinch', 'value': 'p'},
             {'label': 'Package', 'value': 'pkg'},
             {'label': 'Small', 'value': 'sm'},
             {'label': 'Speck', 'value': 'sp'},
             {'label': 'Slice', 'value': 'sl'}]
}

food_columns = ['index', 'domain', 'name', 'portion', 'unit', 'calories', 'fat', 'cholesterol', 'sodium', 'carbohydrate', 'protein']

df0 = get_table_data(table='food', columns=food_columns, servings=True)


layout = html.Div(id='main',
    className='container-xl',
    children=[
        dcc.Store(id='user-store'),
        html.H1(id='username'),
        html.H1(id='meal-food', children='Meals and Food Data'),
        dropdown_input(name='scope',
            className='meal',
            value='Last 24 hours',
            btn_dict=BTN_DICT),
        html.Br(),
        dbc.Form(id='meal',
            children=[
                user_input(name='timestamp',
                    className='meal',
                    type='text',
                    placeholder='Date & Time.',
                    required=False,
                    value=arrow.now().format("YYYY-MM-DD HH:mm")),
                user_input(name='calories',
                    className='meal',
                    type='number',
                    placeholder='Calories',
                    required=False,
                    value=None),
                user_input(name='fat',
                    className='meal',
                    type='number',
                    placeholder='Fat',
                    required=False,
                    value=None),
                user_input(name='cholesterol',
                    className='meal',
                    type='number',
                    placeholder='Cholesterol',
                    required=False,
                    value=None),
                user_input(name='sodium',
                    className='meal',
                    type='number',
                    placeholder='Sodium',
                    required=False,
                    value=None),
                user_input(name='carbohydrate',
                    className='meal',
                    type='number',
                    placeholder='Carbohydrate',
                    required=False,
                    value=None),
                user_input(name='protein',
                    className='meal',
                    type='number',
                    placeholder='Protein',
                    required=False,
                    value=None),
                user_input(name='servings',
                    className='meal',
                    type='text',
                    placeholder='Servings',
                    required=False,
                    value=None),
                user_input(name='indices',
                    className='meal',
                    type='text',
                    placeholder='Indices',
                    required=False,
                    value=None),
                form_buttons(name='submit',
                    className='meal',
                    children='Submit Meal')
            ]
        ),
        html.Br(),
        dash_table.DataTable(
            id='food-table',
            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            data=df0.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df0.columns],
            editable=True,
            filter_action='native',
            sort_action='native',
            sort_mode='multi',
            column_selectable=False,
            row_deletable=False,
            row_selectable='multi',
            selected_columns=[],
            selected_rows=[]
        )
    ]
)
