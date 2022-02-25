import arrow as Arw
import dash_bootstrap_components as dbc
from dash import dcc, html

dropdown = dbc.DropdownMenu(
    label="Data Scope",
    id='data-scope',
    class_name='dropdown',
    menu_variant='dark',
    children=[
        dbc.DropdownMenuItem('Last 24 hours.'),
        dbc.DropdownMenuItem('Last 14 days.'),
        dbc.DropdownMenuItem('Last 90 days.')
    ]
)

event_type_group = dbc.ButtonGroup(
    dbc.DropdownMenu(
        label='Event Type',
        id='event-type',
        class_name='dropdown',
        menu_variant='dark',
        group=True,
        children=[
            dbc.DropdownMenuItem('No Special Event'),
            dbc.DropdownMenuItem('Bolus Insulin'),
            dbc.DropdownMenuItem('Basal Insulin'),
            dbc.DropdownMenuItem('Meal'),
            dbc.DropdownMenuItem('Medication'),
            dbc.DropdownMenuItem('Execrise')
        ]
    )
)

message_input_group = html.Div(id='message', children=[
    dbc.DropdownMenu(
        label="Message",
        id='message-input',
        className='dropdown',
        menu_variant='dark',
        group=True,
        children=[
            dbc.DropdownMenuItem('No alarm.'),
            dbc.DropdownMenuItem('Glucose is low.'),
            dbc.DropdownMenuItem('Glucose is going low.'),
            dbc.DropdownMenuItem('My glucose low alarm.'),
            dbc.DropdownMenuItem('My glucose high alarm.'),
            dbc.DropdownMenuItem('Glucose is going high.'),
            dbc.DropdownMenuItem('Glucose is high.')
        ]
    )
])

trend_input_group = html.Div(id='trend-input', children=[
    dbc.DropdownMenu(
        label='Trend',
        id='trend-arrow',
        className='dropdown',
        menu_variant='dark',
        group=True,
        children=[
            dbc.DropdownMenuItem('The arrow is pointing right.'),
            dbc.DropdownMenuItem('The arrow is pointing down.'),
            dbc.DropdownMenuItem('The arrow is pointing down and right.'),
            dbc.DropdownMenuItem('The arrow is pointing up and right.'),
            dbc.DropdownMenuItem('The arrow is pointing up.')
        ]
    )
])

glucose_input = html.Div(id='glucose-input', children=[
    dbc.Input(id='glucose-intput-number', type='number', placeholder='Blood Sugar Level', required=True)
])

ts_input = html.Div(id='ts-input', children=[
    dbc.Label(id='ts-label', children=['Date Time']),
    dbc.Input(id='timetamp-input', type='text', value=Arw.now().format("YYYY-MM-DD HH:mm"))
])

bolus_unit_input = html.Div(id='bolus-unit-input', children=[
    dbc.Label(id='bolus-unit-label', children=['Bolus (meal) insulin.']),
    dbc.Input(id='bolus-unit-number', type='number', value=0)
])

basal_unit_input = html.Div(id='basal-unit-input', children=[
    dbc.Label(id='basal-unit-label', children=['Basal (background) insulin']),
    dbc.Input(id='basal-unit-number', type='number', value=0),
    html.Br(),
    html.P(id='basal-unit-output')
])

carbohydrate_input = html.Div(id='carbohydrate-input', children=[
    dbc.Label(id='carbohydrate-label', children=['Carbohydrates consumed.']),
    dbc.Input(id='carbohydrate-number', type='number', value=0)
])

notes_input = html.Div(id='notes-input', children=[
    dbc.Input(id='notes-intput-text', type='text', placeholder='Additional notes for this scan.')
])

layout = html.Div(
    id='main',
    className='container-xl',
    children=[
        dcc.Store(id='user-store'),
        html.H1(id='username', className='card-title', children=[]),
        html.H1(id='bgl', className='card-header', children=['Glucose Level']),
        html.Div(id='data-scope-div', className='card-body', children=[dropdown]),
        dbc.Form(id='scan-form', className='g-2', children=[
            dbc.Row(id='scan-form-top-row', children=[
                dbc.Col(id='scan-form-top-row-left', children=[event_type_group]),
                dbc.Col(id='scan-form-top-row-center-left', children=[message_input_group]),
                dbc.Col(id='scan-form-top-row-center-right', children=[trend_input_group]),
                dbc.Col(id='scan-form-top-row-right', children=[glucose_input])]),
            dbc.Row(id='scan-form-middle-row', children=[
                dbc.Col(id='scan-form-middle-row-left', children=[ts_input]),
                dbc.Col(id='scan-form-middle-row-center-left', children=[bolus_unit_input]),
                dbc.Col(id='scan-form-middle-row-center-right', children=[basal_unit_input]),
                dbc.Col(id='scan-form-middle-row-right', children=[carbohydrate_input])
                ]),
            dbc.Row(id='scan-form-bottom-row', children=[notes_input])
        ])
    ]
)
