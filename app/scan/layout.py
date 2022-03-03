"""Dash Application Layout Scan Data"""
from typing import Optional

import arrow
import dash_bootstrap_components as dbc
from dash import dcc, html

BTN_DICT = {
    'scope': ['Last 24 hours', 'Last 14 days', 'Last 90 days'],
    'event': ['No Special Event', 'Medication', 'Execrise'],
    'message': ['Is high', 'Is going high', 'My high alarm', 'No alarm', 'My low alarm', 'Is going low', 'Is low'],
    'trend': ['Pointing up', 'Pointing up and right', 'Pointing right', 'Pointing down and right', 'Pointing down']
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
            children='Glucose Level Scan'
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
        dbc.Form(
            id='scan',
            children=[
                dbc.Row(
                    id='top-row',
                    children=[
                        dbc.Col(
                            id='top-row-left',
                            children=dropdown_input(
                                name='event',
                                className='dropdown',
                                value='No Special Event'
                            )
                        ),
                        dbc.Col(
                            id='top-row-center-left',
                            children=dropdown_input(
                                name='message',
                                className='dropdown',
                                value='No alarm'
                            )
                        ),
                        dbc.Col(
                            id='top-row-center-right',
                            children=dropdown_input(
                                name='trend',
                                className='dropdown',
                                value='Pointing right'
                            )
                        ),
                        dbc.Col(
                            id='top-row-right',
                            children=user_input(
                                name='glucose',
                                className='input',
                                type='number',
                                placeholder='Glucose Reading.',
                                required=True,
                                value=None
                            )
                        )
                    ]),
                html.Br(),
                dbc.Row(id='middle-row', children=[
                    dbc.Col(
                        id='middle-row-left',
                        children=user_input(
                            name='timetamp',
                            className='input',
                            type='text',
                            placeholder='Date & Time.',
                            required=False,
                            value=arrow.now().format("YYYY-MM-DD HH:mm")
                        )
                    ),
                    dbc.Col(
                        id='middle-row-center-left',
                        children=user_input(
                            name='bolus_unit',
                            className='input',
                            type='number',
                            placeholder='Bolus Insulin (meal)',
                            required=False,
                            value=None
                        )
                    ),
                    dbc.Col(
                        id='middle-row-center-right',
                        children=user_input(
                            name='basal_unit',
                            className='input',
                            type='text',
                            placeholder='Basal Insulin (background)',
                            required=False,
                            value=None
                        )
                    ),
                    dbc.Col(
                        id='middle-row-right',
                        children=user_input(
                            name='carbohydrate',
                            className='input',
                            type='number',
                            placeholder='CarCarbohydrates consumed',
                            required=False,
                            value=None
                        )
                    )
                ]),
                html.Br(),
                dbc.Row(
                    id='bottom-row',
                    children=user_input(
                        name='notes',
                        className='input',
                        type='text',
                        placeholder='Additional notes.',
                        required=False,
                        value=None
                    )
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
)
