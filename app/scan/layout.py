"""Scan Dash Application Layout"""
import arrow
import dash_bootstrap_components as dbc
from dash import dcc, html
from .assets.utils import dropdown_input, form_buttons, user_input

BTN_DICT = {
    'scope': ['Last 24 hours', 'Last 14 days', 'Last 90 days'],
    'event': ['No Special Event', 'Medication', 'Execrise'],
    'message': ['Is high', 'Is going high', 'My high alarm', 'No alarm', 'My low alarm', 'Is going low', 'Is low'],
    'trend': ['Pointing up', 'Pointing up and right', 'Pointing right', 'Pointing down and right', 'Pointing down']
}


layout = html.Div(
    id='main',
    className='scan',
    children=[
        dcc.Store(id='user-store'),
        html.P(id='username'),
        html.H3(id='bgl',
            className='scan',
            children='Blood Glucose Level Scan'),
        dropdown_input(name='scope',
            className='scan',
            value='Last 24 hours',
            btn_dict=BTN_DICT),
        dbc.Form(id='scan',
            children=[
                user_input(name='timetamp',
                    className='scan',
                    type='text',
                    placeholder='Date & Time.',
                    required=False,
                    value=arrow.now().format("YYYY-MM-DD HH:mm")),
                dropdown_input(name='message',
                    className='scan',
                    value='No alarm',
                    btn_dict=BTN_DICT),
                dropdown_input(name='trend',
                    className='scan',
                    value='Pointing right',
                    btn_dict=BTN_DICT),
                user_input(name='glucose',
                    className='scan',
                    type='number',
                    placeholder='Glucose Reading.',
                    required=True,
                    value=None),
                user_input(name='bolus_unit',
                    className='scan',
                    type='number',
                    placeholder='Bolus Insulin (meal)',
                    required=False,
                    value=None),
                user_input(name='basal_unit',
                    className='scan',
                    type='text',
                    placeholder='Basal Insulin (background)',
                    required=False,
                    value=None),
                user_input(name='carbohydrate',
                    className='scan',
                    type='number',
                    placeholder='Carbohydrates consumed',
                    required=False,
                    value=None),
                dropdown_input(name='event',
                    className='scan',
                    value='No Special Event',
                    btn_dict=BTN_DICT),
                user_input(name='notes',
                    className='scan',
                    type='text',
                    placeholder='Additional notes.',
                    required=False,
                    value=None),
                form_buttons(name='submit',
                    className='scan',
                    children='Submit')
            ]
        )
    ]
)
