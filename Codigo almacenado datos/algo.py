import os
import webbrowser
from threading import Thread
import pyautogui
import dash
from jupyter_dash import JupyterDash
from dash import dcc as dcc
from dash import html as html
import plotly
from dash.dependencies import Input, Output
import random
import plotly.graph_objs as go
from datetime import datetime as dt

alt, anch= pyautogui.size()



app = dash.Dash()

app.external_stylesheets = [
    "/static/reset.css"
]
app.server.static_folder = 'static'
app.layout = html.Div([
                    html.Video(src="/static/InicioCoche.mp4",
                                autoPlay='autoPlay',loop=False,muted='muted')
                    ])

server=app.server

@server.route('/static/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(os.path.join(root_dir, 'static'), path)


if __name__ == '__main__':
    app.run_server(debug=True)