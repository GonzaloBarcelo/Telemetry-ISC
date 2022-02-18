from collections import deque
import csv
import dash
import pandas as pd
from jupyter_dash import JupyterDash
from dash import dcc as dcc
from dash import html as html
import plotly
import plotly.express as px
from dash.dependencies import Input, Output, State
import random
import webbrowser
import plotly.graph_objs as go
import os
import flask 

def lastValuetxt(idm):
    with open(str(idm)+".txt","r") as file:
        values=[]
        for i in file:
            values.append(i)
        valor=values[len(values)-1].split()

        return toFloat(valor[2])
    
def toFloat(value):
    num=[]
    number=["0","1","2","3","4","5","6","7","8","9",".",","]
    coma=5
    ajust=coma
    for i in value:
        if i not in value or coma==0:
            break
        else:
            if i==".":
                coma=ajust-1
            if coma!=ajust:
                coma=coma-1
            num.append(i)
    return float("".join(num))

def getValues(idmBat):
    temps=[]
    for i in idmBat:
        temps.append(lastValuetxt(i))
    return temps

def getBatteriesCritic(temps):
    critic=[]
    for i in temps:
        if i>=90:
            critic.append(1)
        else:
            critic.append(0)
    return critic



idm=[100,101,102,110,111,112,130,131,132,133,134,140,141,142,143,144]
#idm=[100,101,102,110,111,112,134]
idm=[]
variables=["Tension Inversor","Temperatura motor","Temperatura inversor",
        "Temperatura Refri In","Temperatura Refri Out","Presion Aero Refri","Aceleracion Pedal",    
        "Acelerometro X","Acelerometro Y","Acelerometro Z",
        "Presion Frenos", "Temperatura Baterias 1","Temperatura Baterias 2",
        "Temperatura Baterias 3","Temperatura Baterias 4","Temperatura Baterias 5"]

colors = {
    'background': '#000000',
    'text': '#7FDBFF'
}


app = dash.Dash(__name__)


app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    #html.Div([
    #    html.H4('Datos Coche')
    #    ]),
    
    html.Div([
        dcc.Graph(id='live-update-graph-acelerometer',
            config={'displayModeBar':False})
    ], style= {'height':'40%','width': '29%', 'display': 'inline-block'}),

        html.Div([
        dcc.Graph(id='live-update-graph-Potencia')
    ], style= {'height':'40%','width': '10%', 'display': 'inline-block'}),


    html.Div([
        dcc.Graph(id='live-update-graph-refri')
    ], style= {'height':'40%','width': '20%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='live-update-graph-RPM')
    ], style= {'height':'40%','width': '10%', 'display': 'inline-block'}),


     html.Div([
        dcc.Graph(id='live-update-graph-bateries')
    ], style= {'height':'40%','width': '30%', 'display': 'inline-block'}),


    html.Div([
        dcc.Graph(id='live-update-graph-aceleracion')
    ], style= {'height':'20vh','width': '30%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='live-update-graph-tensionInversor')
    ], style= {'height':'20vh','width': '40%', 'display': 'inline-block'}),

   
    html.Div([
        dcc.Graph(id='live-update-graph-tempmotorinv')
    ], style= {'height':'20vh','width': '30%', 'display': 'inline-block'}),

    html.Div([
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1*1500, # in milliseconds
            n_intervals=0
            ),
        dcc.Interval(
            id='interval-bateries',
            interval=1*5000, # in milliseconds
            n_intervals=0
            ),
        dcc.Interval(
            id='interval-refri',
            interval=1*2000, # in milliseconds
            n_intervals=0
            )
        
        ]),

])


###Temperatura Motor e Inversor

@app.callback(Output('live-update-graph-tempmotorinv', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    df=pd.DataFrame({
        "Temperatura":["Motor","Inversor","Aire"],
        "ºC":getValues([101,102,103])
        })

    fig=px.bar(df,x="ºC",y="Temperatura",orientation="h")
    

    fig.update_layout(
    autosize=True,
    #width=1800,
    height=100,
    margin=dict(
        l=5,
        r=2,
        b=1,
        t=1,
        pad=4
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    fig.update_xaxes(range=[0,100])


    return fig

### RPM
@app.callback(Output('live-update-graph-RPM', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    df=pd.DataFrame({
        "v":["RPM"],
        "n":getValues([104])
        })

    fig=px.bar(df,x="v",y="n",orientation="v")

    fig.update_layout(
    autosize=True,
    #width=1800,
    height=350,
    margin=dict(
        l=5,
        r=20,
        b=1,
        t=1,
        pad=4
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    fig.update_yaxes(range=[0,5500])

    return fig


### Potencia
@app.callback(Output('live-update-graph-Potencia', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    df=pd.DataFrame({
        "W":["Potencia"],
        "P":getValues([105])
        })

    fig=px.bar(df,x="W",y="P",orientation="v")

    fig.update_layout(
    autosize=True,
    #width=1800,
    height=350,
    margin=dict(
        l=5,
        r=5,
        b=1,
        t=1,
        pad=4
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    fig.update_yaxes(range=[0,5500])

    return fig


### Texto

@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    datos_plot=[]
    for  i in idm:
        datos_plot.append(lastValuetxt(i))
    lista_a_ret=[]

    style = {'padding': '5px', 'fontSize': '20px'}
    for i in range(len(idm)):
        lista_a_ret.append(html.Span(str(variables[i])+':{0:.3f}'.format(datos_plot[i]),style=style))
    return lista_a_ret

###Baterias

@app.callback(Output('live-update-graph-bateries', 'figure'),
              Input('interval-bateries', 'n_intervals'))
def update_graph_live(n):

    temps=getValues([140,141,142,143,144])
    critic=getBatteriesCritic(temps)
    df=pd.DataFrame({
        "Baterias":["1","2","3","4","5"],
        "Temperatura":temps,
        "Critical":critic
        })

    fig=px.bar(df,x="Baterias",y="Temperatura",color="Critical")
    #fig=px.bar(df,x="Baterias",y="Temperatura")

    fig.update_layout(
    autosize=True,
    #width=1800,
    height=350,
    margin=dict(
        l=5,
        r=0,
        b=0,
        t=0,
        pad=4
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    fig.update_yaxes(range=[0,100])

    return fig




####Tension-Inversor

@app.callback(Output('live-update-graph-tensionInversor', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):


    df=pd.DataFrame({
        "Inversor":["Inversor"],
        "Tension":getValues([100])
        })

    fig=px.bar(df,x="Tension",y="Inversor",orientation="h")

    fig.update_layout(
    autosize=True,
    #width=1800,
    height=100,
    margin=dict(
        l=5,
        r=20,
        b=1,
        t=1,
        pad=4
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    fig.update_xaxes(range=[0,400])

    return fig


####Aceleracion

@app.callback(Output('live-update-graph-aceleracion', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    df=pd.DataFrame({
        "Aceleracion":["Pedal"],
        "%":getValues([133])
        })

    fig=px.bar(df,x="%",y="Aceleracion",orientation="h")

    fig.update_layout(
    autosize=True,
    #width=1800,
    height=120,
    margin=dict(
        l=5,
        r=20,
        b=1,
        t=1,
        pad=4
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    fig.update_xaxes(range=[0,100])

    return fig



####Acelerometros

@app.callback(Output('live-update-graph-acelerometer', 'figure'),
              Input('interval-refri', 'n_intervals'))
def update_graph_live(n):

    df=pd.DataFrame({
        "Acelerometer":["X","Y","Z"],
        "%":getValues([130,131,132])
        })

    fig=px.bar(df,x="Acelerometer",y="%")

    fig.update_layout(
    autosize=True,
    #width=1800,
    height=350,
    margin=dict(
        l=2,
        r=20,
        b=1,
        t=1,
        pad=4
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    fig.update_yaxes(range=[0,100])

    return fig


###Refri

@app.callback(Output('live-update-graph-refri', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    df=pd.DataFrame({
        "Refri":["In","Out","Pre"],
        "%":getValues([110,111,112])
        })

    fig=px.bar(df,x="Refri",y="%",orientation="v")

    fig.update_layout(
    autosize=True,
    #width=1800,
    height=350,
    margin=dict(
        l=5,
        r=5,
        b=1,
        t=1,
        pad=4
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    fig.update_yaxes(range=[0,100])

    return fig



if __name__ == '__main__':
    app.run_server(debug=True, port =1111)