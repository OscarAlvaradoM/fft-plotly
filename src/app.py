import plotly.graph_objects as go

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html

import utils
from styles import COLORS_STYLE, SIDEBAR_STYLE, CONTENT_STYLE, UPLOAD_STYLE, INITIAL_CONTENT_STYLE

df_datos_medidos = None
df_fourier = None
axes_1, axes_2 = utils.get_empty_axes()
fig = utils.get_fig(axes_1, axes_2, df_datos_medidos)

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

# Aquí definimos la plantilla inicial. Habría que colocar todos los elementos que queremos de principio y serán los que se irán actualizando.
app.layout = html.Div([sidebar, utils.initial_content()])

# ------------------------------------------ Callbacks -----------------------------------------------------------------------

@app.callback(Output('output-data-upload', 'children'), # -> Es el componente que estoy editando desde acá
              Output('muestras', 'style'),              # -> El estado de visibilidad del número de muestras
              Output('numero-muestras', 'value'),       # -> El valor de las muestras
              Input('upload-data', 'contents'),         # -> Archivo
              State('upload-data', 'filename'))
def update_output(content, filename):
    if content:
        global df_datos_medidos, df_fourier
        df_datos_medidos, df_fourier, axes_1, axes_2 = utils.parse_contents(content, filename)
        fig, number_samples = utils.get_fig(axes_1, axes_2, df_datos_medidos)
        children = utils.valid_content(fig, filename)
        style = {'display': 'block'}
    else:
        children = utils.initial_content()
        style = {'display': 'None'}
        number_samples = None
    return children, style, number_samples

@app.callback(Output('graficas', 'figure'),        # -> Es el componente que estoy editando desde acá
              Input('numero-muestras', 'value'))    # -> El dcc.Input
def update_input_number_samples(number_samples):
    global df_datos_medidos, df_fourier
    if number_samples:
        df_datos_medidos_changed, df_fourier_changed = utils.change_number_samples(df_datos_medidos, df_fourier, number_samples)
        axes_1, axes_2 = utils.get_axes(df_datos_medidos_changed, df_fourier_changed)
        fig, _ = utils.get_fig(axes_1, axes_2, df_datos_medidos_changed)

        return fig

if __name__ == '__main__':
    app.run_server(debug=True)