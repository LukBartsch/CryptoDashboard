import dash
from layouts import layout
import callbacks



app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.layout = layout
server = app.server

if __name__ == '__main__':
    app.run_server()