from app import app
from layout.main_layout import layout
import callbacks


app.layout = layout
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)