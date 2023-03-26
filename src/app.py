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

colors = {"text_color": "#D8D8D8",
          "background_color_1": "#1E1E1E",
          "background_color_2": "#323130"}

# El estulo para el panel de la izquierda.
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": colors["background_color_1"]
}

# El estilo para el contenido principal, es decir, donde se encontrarán las gráficas.
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    "background-color": colors["background_color_2"]
}

# El estilo para el botón de carga de archivos.
UPLOAD_STYLE = {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '5px',
            'color': colors["text_color"]
        }

upload_object = dcc.Upload(
        id='upload-data',
        children=html.Div(['Arrastra y suelta o ', html.A('Selecciona archivos')]),
        style=UPLOAD_STYLE,
        # Vemos si podemos escoger múltiples archivos a la vez. Por el momento no queremos esto.
        multiple=False
    )

sidebar = html.Div(
    [
        html.H2("Ondas", className="display-4", style={"color":colors["text_color"]}),
        html.Hr(style={"color":colors["text_color"]}),
        html.P("Selecciona el archivo que quieras visualizar:", className="lead", style={"color":colors["text_color"]}),
        upload_object,
        html.Br(),
        dbc.Nav(
            [
                dbc.NavLink("FFT", href="/", active="exact", style={"text-align":"center"}),
                dbc.NavLink("Histograma", href="/page_1", active="exact", style={"text-align":"center"})
            ],
            vertical=False,
            pills=True,
            justified=True
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Aquí está el contenido de la página principal, es decir, donde se encontrarán las gráficas.
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

    except Exception as e:
        print(e)
        return html.Div([
            'Hubo un error procesando este archivo, por favor asegúrate que es un archivo de tipo .csv o .xls'
        ])

    fig = onda.plot_fourier()

    return html.Div([
        html.H5(f"Archivo seleccionado: {filename}", style={"color":colors["text_color"]}),

       dcc.Graph(figure=fig, id='onda_original'),
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, name):
    if contents:
        children = parse_contents(contents, name)
        return children

if __name__ == '__main__':
    app.run_server(debug=True)