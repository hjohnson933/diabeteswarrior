from dash import html  # , dcc, dash_table

from app import BaseConfig

layout = html.Div([
    html.P(BaseConfig.SQLALCHEMY_DATABASE_URI)
])
