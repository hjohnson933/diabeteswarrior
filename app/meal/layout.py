"""Dash Application Layout Scan Data"""
import dash_bootstrap_components as dbc
from dash import dcc, html

from .assets.utils import dropdown_input, form_buttons

BTN_DICT = {
    'scope': ['Last 24 hours', 'Last 14 days', 'Last 90 days']
}


layout = html.Div(
    id='main',
    className='container-xl',
    children=[
        dcc.Store(
            id='user-store'
        ),
        html.H1(
            id='username'
        ),
        html.H1(
            id='bgl',
            children='Meals and Food Data'
        ),
        dropdown_input(
            name='scope',
            className='dropdown',
            value='Last 24 hours'
        ),
        html.Div('Meal Feedback'),
        dbc.Form(
            id='food',
            children=[
                dbc.Row(
                    id='top-row',
                    children=[
                        dbc.Col(
                            id='top-row-left',
                            children=[]
                        ),
                        dbc.Col(
                            id='top-row-center-left',
                            children=[]
                        ),
                        dbc.Col(
                            id='top-row-center-right',
                            children=[]
                        ),
                        dbc.Col(
                            id='top-row-right',
                            children=[]
                        )
                    ]
                ),
                html.Br(),
                dbc.Row(
                    id='button-row',
                    children=[
                        dbc.Col(
                            id='button-row-left'
                        ),
                        dbc.Col(
                            id='button-row-center',
                            children=form_buttons(
                                name='submit',
                                className='button',
                                children='Submit'
                            )
                        ),
                        dbc.Col(
                            id='button-row-right'
                        )
                    ]
                )
            ]
        ),
        html.Div(
            id='food-table',
            className='food',
            children='food_table()'
        )
    ]
)
