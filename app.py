import os
from dotenv import load_dotenv
from pathlib import Path
import dash
import dash_bootstrap_components as dbc


base_dir = Path(__file__).resolve().parent
env_file = base_dir / '.env'
load_dotenv(env_file)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True