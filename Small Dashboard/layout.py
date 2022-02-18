import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import plotly.express as px

###TODO ESTO ES EL LAYOUT
# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'right': 0,
    'bottom': 300,
    'width': '35%',
    'padding': '20px 10p'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'top': 0,
    'left': 0,
    'bottom': 0,
    "width": "100%",
    'padding': '20px 10p'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

GRAPH_HORIZONTAL_STYLE = {
    "width":"100%",
    "height":"300px",
    "orientation":"h"
}

GRAPH_VERTICAL_STYLE = {
    "width":"90%",
    "height":"100%",
    "orientation":"v"
}

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_velocity', style = GRAPH_HORIZONTAL_STYLE), md=7
        )
    ]
)

content_third_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_battery', style =GRAPH_HORIZONTAL_STYLE), md=12,
        )
    ]
)



content_header = dbc.Row(   
    [   
        dbc.Col(html.Img(
                src="https://media-exp1.licdn.com/dms/image/C4D0BAQGHF86BLbWa0w/company-logo_200_200/0/1631298662767?e=2159024400&v=beta&t=MlxW8mKTYRLeWnb2i6N2aJJHup0Ta0jDFch4f91iLxU",
                style={
                    'height': '70px',
                    'width': '70px',
                    'float': 'left',
                    'position': 'relative',
                },
                
            ), md =1),
        dbc.Col(
            html.H1('35º', style=TEXT_STYLE), md=1
        ),
        dbc.Col(
            html.H1("40º", style = TEXT_STYLE), md=1
        ),
        dbc.Col(
            html.H1("55º", style = TEXT_STYLE), md=1
        )
    ]
)


content = html.Div(
    [   
        html.Br(),
        content_header,
        content_second_row,
        content_third_row
    ],
    style=CONTENT_STYLE
)



modulo = dbc.Row([
    dbc.Col(
        dcc.Graph(id='graph_accelerator', style = GRAPH_VERTICAL_STYLE), md=6),
    dbc.Col(
        dcc.Graph(id='graph_brake', style = GRAPH_VERTICAL_STYLE), md=6),


    ])


sidebar = html.Div(
    [ 
        modulo
            ],
            style= SIDEBAR_STYLE
)

update = html.Div([
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
            )
        ])

warning = dbc.Modal(
    [
        dbc.ModalHeader("Error"),
        dbc.ModalBody(id="update-error"),
        dbc.ModalFooter(
            dbc.Button("Close", id = "close", className="ml-auto",n_clicks=0 ),
        ),
        ],
        id = 'modal',
        is_open= True,

    )

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([ content, sidebar, update, warning])

## AQUI EMPEZARÍAN LOS CALLBACKS

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


if __name__ == '__main__':
    app.run_server(port='8085',debug=True, threaded=True)