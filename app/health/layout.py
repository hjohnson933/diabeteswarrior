"""Dash Application Layout Health Data"""
import arrow
import dash_bootstrap_components as dbc
from dash import dcc, html
from .assets.utils import dropdown_input, form_buttons, user_input

BTN_DICT = {
    'scope': ['Last 24 hours', 'Last 14 days', 'Last 90 days'],
    'ihb': ['Regular Heart Beat', 'Irregular Heart Beat'],
    'stage': ['No Hypertension', 'Pre-Hypertension', 'Stage I Hypertension', 'Stage II Hypertension']
}


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
            id='health',
            className='card-header',
            children='General Health Information'
        ),
        html.Div(
            id='data-scope',
            className='card-body',
            children=dropdown_input(
                name='scope',
                className='dropdown',
                value='Last 24 hours',
                btn_dict=BTN_DICT
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
                            id='bpc-heartbeat',
                            children=dropdown_input(
                                name='ihb',
                                className='dropdown',
                                value='Regular Heart Beat',
                                btn_dict=BTN_DICT
                            )
                        ),
                        dbc.Col(
                            id='bpc-hypertension',
                            children=dropdown_input(
                                name='stage',
                                className='dropdown',
                                value='No Hypertension',
                                btn_dict=BTN_DICT
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
