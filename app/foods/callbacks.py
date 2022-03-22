# import statistics

# import arrow
import flask
# import pandas as pd
from app import BaseConfig
from app.models import Foods, Units, Users
from dash import Input, Output  # , dash_table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

conn = BaseConfig.SQLALCHEMY_DATABASE_URI


def make_data_frame(uid) -> object:
    """ Makes the dictionary of data and returns a pandas data frame

        Parameters
        ----------
            uid : int
                Id of the logged in user

        Returns : object
            Pandas data frame

    """

    engine = create_engine(conn)
    Session = sessionmaker(bind=engine)
    session = Session()
    results = session.query(Foods, Units, Users).\
        filter(Foods.user_id == Users.id).\
        filter(Users.id == uid).all()

    # !
    print(results)
    # result_dict = {}
    # for result in results:
    #     result_dict[result[0].index] = {
    #         'when': arrow.get(result[0].ts, 'US/Central').humanize(),
    #         'username': result[1].username
    #     }

    # rv = pd.DataFrame.from_dict(result_dict, 'index')
    # !
    rv = "Working on make data frame"
    return rv


def register_callbacks(dashapp):
    @dashapp.callback(Output('table-contents', 'children'), Input('table-contents', 'children'))
    def update_output(children):
        # ? Preprocessing
        uid = flask.request.cookies['userID']
        df = make_data_frame(uid)

        # !
        rv = df
        # ? Processing
        # rv = dash_table.DataTable(
        #     data=df.to_dict('records'),
        #     columns=[
        #         {'name': 'exercise', 'id': 'exercise'}
        #     ],
        #     filter_action='native',
        #     page_action='native',
        #     sort_action='native',
        #     page_current=0,
        #     page_size=18,
        #     style_cell={'backgroundColor': 'black', 'font-size': '12px'}
        #     )

        # ? Postprocessing
        return rv
