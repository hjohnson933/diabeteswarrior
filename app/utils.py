"""Diabetes Warrior Utilities."""
from typing import Any, Optional

import dash
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Engine = create_engine('postgresql://hjohnson933:__46_LITTLE_barbados_LATE_76__@git.house.lan:5432/hjohnson933')
Base: Any = declarative_base()


def dropdown_input(name: str, className: str, value: str, btn_dict: dict) -> object:
    """Set a common interface for the dropdown input core component.

    Args:
        name (str): Used to generate the id of the dropdown.
        className (str): Used to generate the class name of the dropdown.
        value (str): Default value for the dropdown if given.
        btn_dict (dict): A dictionary of drop down values.

    Returns:
        object: dash core component.
    """
    return dash.dcc.Dropdown(id=f'{name}-{className}-menu',
        className=className,
        options=btn_dict[name],
        value=value)


def user_input(name: str, className: str, type: str, placeholder: str, required: bool, value: Optional[str]) -> object:
    """Set a common interface for the input core component.

    Args:
        name (str): The element name for the form.
        className (str): CSS class name.
        type (str): The type of input acceptable.
        placeholder (str): Text to display until the data is entered.
        required (bool): Is a value required.
        value (Optional[str]): A list of values if provided.

    Returns:
        object: dash core component.
    """
    return dash.dcc.Input(id=f'{name}-{className}-input',
        name=f'{name}-{className}',
        className=className,
        type=type,
        placeholder=placeholder,
        required=required,
        value=value)


def form_buttons(name: str, className: str, children: str) -> object:
    """Set a common interface for the buttons html component.

    Args:
        name (str): Generat eht element id.
        className (str): CSS class for the element.
        children (str): Sub elements for pass into the button.

    Returns:
        object: A HTML element.
    """
    return dash.html.Button(id=f'{name}-{className}-button',
        className=className,
        children=children)


def nav_home(username: str, className: str) -> str:
    """Set a common top level navigation page for the Dash applications.

    Args:
        username (str): Current users username.
        className (str): CSS class.

    Returns:
        str: A HTML division element.
    """
    return dash.html.Div(id=F"{username}-{className}-div",
        className=className,
        children=[
            dash.html.H1(id=f'{username}-{className}-heading', className=className, children=F'Hi, {username}'),
            dash.html.Hr(),
            dash.html.A(id=f'{username}-{className}-home', className=className, href="/", children="Home "),
            dash.html.A(id=f'{username}-{className}-scan', className=className, href="/scan/", children="Scan "),
            dash.html.A(id=f'{username}-{className}-food', className=className, href="/food/", children="Food "),
            dash.html.A(id=f'{username}-{className}-meal', className=className, href="/meal/", children="Meal "),
            dash.html.A(id=f'{username}-{className}-health', className=className, href="/health/", children="Health ")
        ]
    )


def write_db(records: str, table: str) -> None:
    """Set a common interface for the ORM.

    Args:
        records (str): The new record.
        table (str): The name of the table to write the record to.

    Returns:
        None: Nothing.
    """
    df = pd.DataFrame(data=records)
    df.set_index('index')
    with Engine.begin() as connection:
        df.to_sql(table, con=connection, if_exists='append')


def max_idx(table: str) -> int:
    """Get the maximum value for a tables index.

    Args:
        table (str): The name of the table you want to index from.

    Returns:
        int: Maximum record number.
    """
    with Engine.begin() as connection:
        return pd.read_sql(table, connection)['index'].count()


def get_table_data(table: str, columns: list, servings: bool = False) -> object:
    """Set a common interface for the ORM to retreive the data for a given table.

    Args:
        table (str): The name of the table to get.
        columns (list): A list of columns to get.
        servings (bool, optional): If True add the servings column to the data frame. Defaults to False.

    Returns:
        object: A pandas data frame.
    """
    with Engine.begin() as connection:
        df = pd.read_sql(table, connection, columns=columns)
        df.set_index('index')
        if servings:
            df['serving'] = None
    return df
