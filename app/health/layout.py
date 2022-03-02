"""Dash Application Layout Scan Data"""

from typing import Optional

import arrow
import dash_bootstrap_components as dbc
from dash import dcc, html

BTN_DICT = {
    'scope': ['Last 24 hours', 'Last 14 days', 'Last 90 days'],
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


layout = html.Div(
    id='main',
    className='container-xl',
    children=[
        dcc.Store(id='user-store'),
        html.H1(id='username', className='card-title'),
        html.H1(id='bgl', className='card-header', children='Health Data'),
        html.Div(id='data-scope', className='card-body', children=dropdown_input(name='scope', className='dropdown', value='Last 24 hours')),
        dbc.Form(id='health-form', children=[
            dbc.Row(
                id='health-form-pulseox-row',
                children=[
                    dbc.Col(id='health-form-pulseox-pulse', children=[]),
                    dbc.Col(id='health-form-pulseox-oxygen', children=[]),
                ]),
            html.Br(),
            dbc.Row(id='health-form-scale-row', children=[
                dbc.Col(id='health-form-scale-weight', children=[]),
                dbc.Col(id='health-form-form-bmi'),
            ]),
            html.Br(),
            dbc.Row(id='health-form-bpcuff-row', children=[
                dbc.Col(id='', children=[]),
                dbc.Col(id='', children=[]),
                dbc.Col(id='', children=[]),
                dbc.Col(id='', children=[]),
                ]),
            html.Br(),
            dbc.Row(id='health-form-thermometer-row', children=[
                dbc.Col(id='scan-form-middle-row-left', children=user_input('timetamp', 'input', 'text', 'Date & Time.', False, arrow.now().format("YYYY-MM-DD HH:mm"))),
                ]),
            html.Br(),
            dbc.Row(id='button-row', children=[
                dbc.Col(id='button-row-left'),
                dbc.Col(id='button-row-center', children=form_buttons('submit', 'button', 'Submit')),
                dbc.Col(id='button-row-right')
            ])
        ])
    ]
)
