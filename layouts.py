import dash_table
import dash_core_components as dcc
import dash_html_components as html

from datetime import datetime
from datetime import timedelta

# from common import COLORS
# from common import BASE_CURRENCIES
# from common import TODAY_DATE


layout = html.Div(className="Main", children=[

    html.H1(
        children="Dash application for cryptocurrencies monitoring",
        className="Main-Header"
    )

])