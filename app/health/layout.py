"""Health Dash Application Layout"""
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
    className='health',
    children=[
        dcc.Store(id='user-store'),
        html.P(id='username'),
        html.H1(id='hlth', children='General Health Information'),
        dropdown_input(name='scope',
            className='health',
            value='Last 24 hours',
            btn_dict=BTN_DICT),
        dbc.Form(
            id='health',
            children=[
                user_input(name='timetamp',
                    className='health',
                    type='text',
                    placeholder='Date & Time.',
                    required=False,
                    value=arrow.now().format("YYYY-MM-DD HH:mm")),
                user_input(name='po_pulse',
                    className='health',
                    type='number',
                    placeholder='Pulseoximeter Pulse',
                    required=True,
                    value=None),
                user_input(name='po_ox',
                    className='health',
                    type='number',
                    placeholder='Oxygen Saturation',
                    required=True,
                    value=None),
                user_input(name='weight',
                    className='health',
                    type='number',
                    placeholder='Weight',
                    required=True,
                    value=None),
                user_input(name='fat',
                    className='health',
                    type='number',
                    placeholder='Fat%',
                    required=True,
                    value=None),
                user_input(name='bpc_pulse',
                    className='health',
                    type='number',
                    placeholder='Pulse',
                    required=True,
                    value=None),
                user_input(name='bpc_systolic',
                    className='health',
                    type='number',
                    placeholder='Systolic',
                    required=True,
                    value=None),
                user_input(name='bpc_diastolic',
                    className='health',
                    type='number',
                    placeholder='Diastolic',
                    required=True,
                    value=None),
                dropdown_input(name='ihb',
                    className='health',
                    value='Regular Heart Beat',
                    btn_dict=BTN_DICT),
                dropdown_input(name='stage',
                    className='health',
                    value='No Hypertension',
                    btn_dict=BTN_DICT),
                user_input(name='temperature',
                    className='health',
                    type='number',
                    placeholder='Temperature',
                    required=True,
                    value=None),
                form_buttons(name='submit',
                    className='health',
                    children='Submit')
            ]
        )
    ]
)
