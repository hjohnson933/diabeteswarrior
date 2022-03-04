"""Dash Application Layout Scan Data"""
from typing import Optional, Tuple

import arrow
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dash_table, dcc, html

from .ifaces import Engine

BTN_DICT = {
    'scope': ['Last 24 hours', 'Last 14 days', 'Last 90 days']
}


def dropdown_input(name: str, className: str, value: str) -> object:
    return html.Div(
        id=f'{name}-div',
        children=[
            dcc.Dropdown(
                id=f'{name}-{className}-menu',
                className=className,
                options=BTN_DICT[name],
                value=value
            )
        ]
    )


def user_input(name: str, className: str, type: str, placeholder: str, required: bool, value: Optional[str]) -> object:
    return html.Div(
        id=f'{name}-{className}-div',
        children=[
            dcc.Input(
                id=f'{name}-{className}',
                name=f'{name}-{className}',
                className=className,
                type=type,
                placeholder=placeholder,
                required=required,
                value=value
            )
        ]
    )


def form_buttons(name: str, className: str, children: str) -> object:
    return html.Div(id=f'{name}-{className}-div', children=html.Button(id=f'{name}-{className}', className=className, children=children))


def food_table() -> object:
    with Engine.begin() as connection:
        df = pd.read_sql_table('food', connection)
        return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])


layout = html.Div(
    id='main',
    className='container-xl',
    children=[
        dcc.Store(
            id='user-store'
        ),
        html.H1(
            id='username',
            className='card-title'
        ),
        html.H1(
            id='bgl',
            className='card-header',
            children='Meals and Food Data'
        ),
        html.Div(
            id='data-scope',
            className='card-body',
            children=dropdown_input(
                name='scope',
                className='dropdown',
                value='Last 24 hours'
            )
        ),
        html.Div(
            id='meal-output',
            className='meal',
            children=['Meal Feedback']
        ),
        html.Div(
            id='new-food',
            className='food',
            children=[
                dbc.Form(
                    id='scan',
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
                )
            ]
        ),
        html.Div(
            id='food-table',
            className='food',
            children=food_table()
        )
    ]
)
