from typing import Optional, Any
import dash
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Engine = create_engine('postgresql://hjohnson933:__46_LITTLE_barbados_LATE_76__@git.house.lan:5432/hjohnson933')
Base: Any = declarative_base()


def dropdown_input(name: str, className: str, value: str, btn_dict: dict) -> object:
    return dash.dcc.Dropdown(
        id=f'{name}-{className}-menu',
        className=className,
        options=btn_dict[name],
        value=value
    )


def user_input(name: str, className: str, type: str, placeholder: str, required: bool, value: Optional[str]) -> object:
    return dash.dcc.Input(
        id=f'{name}-{className}',
        name=f'{name}-{className}',
        className=className,
        type=type,
        placeholder=placeholder,
        required=required,
        value=value
    )


def form_buttons(name: str, className: str, children: str) -> object:
    return dash.html.Button(
        id=f'{name}-{className}',
        className=className,
        children=children
    )


def form_checkbox(name: str, className: str, options: str, btn_dict: dict) -> object:
    return dash.dcc.Checklist(
        id=f'{name}-{className}',
        options=btn_dict[options],
        inline=True
    )
