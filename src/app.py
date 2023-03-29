import base64
import io

import plotly.graph_objects as go

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html

import utils
from styles import COLORS_STYLE, SIDEBAR_STYLE, CONTENT_STYLE, UPLOAD_STYLE, INITIAL_CONTENT_STYLE

import pandas as pd

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Con esto inicializamos la aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# -------------------------------- Objetos base------------------------------------------------------------------------------------
upload_object = dcc.Upload(
        id='upload-data',
        children=html.Div(['Arrastra y suelta o ', html.A('Selecciona archivos')]),
        style=UPLOAD_STYLE,
        # Vemos si podemos escoger múltiples archivos a la vez. Por el momento no queremos esto.
        multiple=False
    )

sidebar = html.Div(
    [
        html.H2("Ondas", className="display-4", style={"color":COLORS_STYLE["text_color"]}),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        html.P("Selecciona el archivo que quieras visualizar:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        upload_object,
        html.Br(),
        dbc.Nav(
            [
                dbc.NavLink("FFT", href="/", active="exact", style={"text-align":"center"}),
                dbc.NavLink("Espectrograma", href="/page_1", active="exact", style={"text-align":"center"})
            ],
            vertical=False,
            pills=True,
            justified=True
        ),
        html.Br(),
        html.Div([
        html.P("Número de muestras:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        dcc.Input(placeholder='Ingresa un valor',type='number', value=None, id="numero-muestras")
        ], style={"display":"None"}, id="muestras")
    ],
    style=SIDEBAR_STYLE,
)

# Aquí está el contenido de la página principal, es decir, donde se encontrarán las gráficas.
# content = html.Div(id="output-data-upload", style=CONTENT_STYLE)

initial_content = html.Div([
        html.H5("Seleccione un archivo en el panel de la izquierda.", style={"color":COLORS_STYLE["text_color"]}),
        dcc.Graph(figure=utils.plot_content()[0], id='graficas'),
    ], id="output-data-upload", style=INITIAL_CONTENT_STYLE)

error_content = html.Div([
        html.H5(f'Hubo un error procesando este archivo, por favor asegúrate que es un archivo de tipo .csv o .xls', style={"color":COLORS_STYLE["text_color"]}),
        dcc.Graph(figure=utils.plot_content()[0], id='graficas'),
    ], id="output-data-upload", style=INITIAL_CONTENT_STYLE)

# Aquí definimos la plantilla inicial. Habría que colocar todos los elementos que queremos de principio y serán los que se irán actualizando.
app.layout = html.Div([sidebar, initial_content])

# ---------------------------------------------------------- Funciones ------------------------------------------------------------------------
def plot_valid_content(file_str, filename):
    fig, numero_muestras = utils.plot_content(file_str)
    children = html.Div([
        html.H5(f"Archivo seleccionado: {filename}", style={"color":COLORS_STYLE["text_color"]}),
       dcc.Graph(figure=fig, id='graficas'),
    ])
    return children, numero_muestras

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

    except Exception as e:
        print(e)
        return error_content

    return plot_valid_content(file_str, filename)

def dev_vacio():
    return initial_content

# ------------------------------------------ Callbacks -----------------------------------------------------------------------

@app.callback(Output('output-data-upload', 'children'), # -> Es el componente que estoy editando desde acá
              Output('muestras', 'style'),              # -> El estado de visibilidad del número de muestras
              Output('numero-muestras', 'value'),              # -> El valor de las muestras
              Input('upload-data', 'contents'),         # -> Archivo
              State('upload-data', 'filename'))
def update_output(contents, name):
    if contents:
        children, numero_muestras = parse_contents(contents, name)
        style = {'display': 'block'}
    else:
        children = dev_vacio()
        style = {'display': 'none'}
        numero_muestras = None
    return children, style, numero_muestras

#@app.callback(Output('grafica', 'children'), # -> Es el componente que estoy editando desde acá
#              Input('numero-muestras', 'contents'),         # -> Archivo
#              State('upload-data', 'filename'))


if __name__ == '__main__':
    app.run_server(debug=True)