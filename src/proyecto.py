import base64
import io

import plotly.graph_objects as go

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

import utils

import pandas as pd

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Con esto inicializamos la aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

upload_object = dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrastra y suelta o ',
            html.A('Selecciona archivos')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Vemos si podemos escoger múltiples archivos a la vez. Por el momento no queremos esto.
        multiple=False
    )

sidebar = html.Div(
    [
        html.H2("Ondas", className="display-4"),
        html.Hr(),
        html.P(
            "Selecciona el archivo que quieras visualizar:", className="lead"
        ),
        upload_object,
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

#fig = 
content = html.Div(id="output-data-upload", style=CONTENT_STYLE)

# Aquí definimos la plantilla inicial. Habría que colocar todos los elementos que queremos de principio y serán los que se irán actualizando.
app.layout = html.Div([sidebar, content])

def parse_contents(content, filename):
    """
    Esta función nos sirve para leer el contenido que estamos seleccionando. Se utiliza en el @callback. 
    Con esta función también estamos decidiendo qué hacemos con el archivo que abrimos. 
    
    
    Por el momento se abre la tabla en la página. Para nada queremos esto. 
    Queremos que esta función sólo genere el archivo y que otras funciones hagan cosas con este archivo.
    """
    content_string = content.split(',')[1]

    decoded = base64.b64decode(content_string)
    print("Decoded: ", decoded)
    print("io string: ", io.StringIO(decoded.decode('utf-8')))
    
    try:
        if 'csv' in filename or 'CSV' in filename:
            # Si el usuario está escogiendo un archivo con extensión .csv
            file_str = io.StringIO(decoded.decode('utf-8'))
        elif 'xls' in filename:
            # Si el usuario está escogiendo un archivo con extensión .xls
            file_str = io.BytesIO(decoded)

        

        onda = utils.Onda(file_str)
        metadata = onda.metadata
        data = onda.data
        print(data)
    except Exception as e:
        print(e)
        return html.Div([
            'Hubo un error procesando este archivo, por favor asegúrate que es un archivo de tipo .csv o .xls'
        ])

    fig = onda.plot_fourier()

    return html.Div([
        html.H5(filename),

       dcc.Graph(
        id='onda_original',
        figure=fig
        ),
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, name):
    children = parse_contents(contents, name)
    return children

if __name__ == '__main__':
    app.run_server(debug=True)
0