import arrow as Arw
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


def scan_input(name: str, className: str, type: str, placeholder: str, required: bool, value: str) -> object:
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
        html.H1(id='bgl', className='card-header', children='Glucose Level Scan'),
        html.Div(id='data-scope', className='card-body', children=dropdown_input(name='scope', className='dropdown', value='Last 24 hours')),
        dbc.Form(id='scan-form', children=[
            dbc.Row(
                id='scan-form-top-row',
                children=[
                    dbc.Col(id='scan-form-top-row-left', children=dropdown_input(name='event', className='dropdown', value='No Special Event')),
                    dbc.Col(id='scan-form-top-row-center-left', children=dropdown_input('message', 'dropdown', 'No alarm')),
                    dbc.Col(id='scan-form-top-row-center-right', children=dropdown_input('trend', 'dropdown', 'Pointing right')),
                    dbc.Col(id='scan-form-top-row-right', children=scan_input('glucose', 'input', 'number', 'Glucose Reading.', True, None))
                ]),
            html.Br(),
            dbc.Row(id='scan-form-middle-row', children=[
                dbc.Col(id='scan-form-middle-row-left', children=scan_input('Timetamp', 'input', 'text', 'Date & Time.', False, Arw.now().format("YYYY-MM-DD HH:mm"))),
                dbc.Col(id='scan-form-middle-row-center-left', children=scan_input('bolus_unit', 'input', 'number', 'Bolus Insulin (meal)', False, None)),
                dbc.Col(id='scan-form-middle-row-center-right', children=scan_input('basal_unit', 'input', 'text', 'Basal Insulin (background)', False, None)),
                dbc.Col(id='scan-form-middle-row-right', children=scan_input('carbohydrate', 'input', 'number', 'Carbohydrates consumed', False, None))
            ]),
            html.Br(),
            dbc.Row(id='scan-form-bottom-row', children=[scan_input('notes', 'input', 'text', 'Additional notes.', False, None)]),
            html.Br(),
            dbc.Row(id='button-row', children=[
                dbc.Col(id='button-row-left'),
                dbc.Col(id='button-row-center', children=form_buttons('submit', 'button', 'Submit')),
                dbc.Col(id='button-row-right')
            ])
        ])
    ]
)
