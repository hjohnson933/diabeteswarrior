"""Dash Application Layout Health Data"""
from typing import Optional

import arrow
import dash_bootstrap_components as dbc
from dash import dcc, html

BTN_DICT = {
    'scope': ['Last 24 hours', 'Last 14 days', 'Last 90 days'],
    'ihb': ['Irregular Heart Beat'],
    'stage': ['No Hypertension', 'Pre-Hypertension', 'Stage I Hypertension', 'Stage II Hypertension']
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
    return html.Div(
        id=f'{name}-{className}-div',
        children=html.Button(
            id=f'{name}-{className}',
            className=className,
            children=children
        )
    )


def form_checkbox(name: str, className: str, options: str) -> object:
    return html.Div(
        id=f'{name}-{className}-div',
        children=dcc.Checklist(
            id=f'{name}-{className}',
            options=BTN_DICT[options],
            inline=True
        )
    )


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
            id='health',
            children=[
                dbc.Row(
                    id='pulseoximeter',
                    children=[
                        dbc.Col(
                            id='pulseoximeter-timetamp',
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
                            id='pulseoximeter-pulse',
                            children=user_input(
                                name='po_pulse',
                                className='input',
                                type='number',
                                placeholder='Pulseoximeter Pulse',
                                required=True,
                                value=None
                            )
                        ),
                        dbc.Col(
                            id='pulseoximeter-oxygen',
                            children=user_input(
                                name='po_ox',
                                className='input',
                                type='number',
                                placeholder='Oxygen Saturation',
                                required=True,
                                value=None
                            )
                        )
                    ]
                ),
                html.Br(),
                dbc.Row(
                    id='scale',
                    children=[
                        dbc.Col(
                            id='scale-weight',
                            children=user_input(
                                name='weight',
                                className='input',
                                type='number',
                                placeholder='Weight',
                                required=True,
                                value=None
                            )
                        ),
                        dbc.Col(
                            id='scale-bmi',
                            children=user_input(
                                name='fat',
                                className='input',
                                type='number',
                                placeholder='Fat%',
                                required=True,
                                value=None
                            )
                        )
                    ]
                ),
                html.Br(),
                dbc.Row(
                    id='sphygmomanometer-top',
                    children=[
                        dbc.Col(
                            id='bpc-pulse',
                            children=user_input(
                                name='bpc_pulse',
                                className='input',
                                type='number',
                                placeholder='Pulse',
                                required=True,
                                value=None
                            )
                        ),
                        dbc.Col(
                            id='bpc-systolic',
                            children=user_input(
                                name='bpc_systolic',
                                className='input',
                                type='number',
                                placeholder='Systolic',
                                required=True,
                                value=None
                            )
                        ),
                        dbc.Col(
                            id='bpc-diastolic',
                            children=user_input(
                                name='bpc_diastolic',
                                className='input',
                                type='number',
                                placeholder='Diastolic',
                                required=True,
                                value=None
                            )
                        )
                    ]
                ),
                html.Br(),
                dbc.Row(
                    id='sphygmomanometer-bottom',
                    children=[
                        dbc.Col(
                            id='bpc-ihb',
                            children=form_checkbox(
                                name='bpc_ihb',
                                className='checklist',
                                options='ihb'
                            )
                        ),
                        dbc.Col(
                            id='bpc-hypertension',
                            children=dropdown_input(
                                name='stage',
                                className='input',
                                value=None
                            )
                        ),
                        dbc.Col(
                            id='thermometer',
                            children=user_input(
                                name='temperature',
                                className='input',
                                type='number',
                                placeholder='Temperature',
                                required=True,
                                value=None
                            )
                        ),
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
)
