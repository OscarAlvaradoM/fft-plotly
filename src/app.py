import plotly.graph_objects as go

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html

import utils
from styles import COLORS_STYLE, SIDEBAR_STYLE, CONTENT_STYLE, UPLOAD_STYLE, INITIAL_CONTENT_STYLE

f_sample = None
number_samples = None
resolucion_frecuencia = None
datos_medidos_a_mostrar = None
df_datos_medidos, df_fourier = None, None
fig_datos_medidos, fig_fourier = utils.get_empty_fig(), utils.get_empty_fig(type="Fourier")

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
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        html.Div([
        html.P("Número de muestras:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='numero-muestras', style={"color":COLORS_STYLE["plot_color_1"]}),
        html.P("Frecuencia de muestreo:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='frecuencia-muestreo', style={"color":COLORS_STYLE["plot_color_1"]}),
        html.P("Resolución en frecuencia:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='resolucion-frecuencia', style={"color":COLORS_STYLE["plot_color_2"]})
        ], style={"display":"None"}, id="propiedades")
    ],
    style=SIDEBAR_STYLE,
)

# Aquí definimos la plantilla inicial. Habría que colocar todos los elementos que queremos de principio y serán los que se irán actualizando.
app.layout = html.Div([sidebar, utils.initial_content()])

# ------------------------------------------ Callbacks -----------------------------------------------------------------------
@app.callback(Output('output-data-upload', 'children'), # -> Es el componente que estoy editando desde acá
              Output('propiedades', 'style'),              # -> El estado de visibilidad del número de muestras
              Input('upload-data', 'contents'),         # -> Archivo
              State('upload-data', 'filename'))         # -> Nombre del archivo
def update_output(content, filename):
    if content:
        global df_datos_medidos, df_fourier, fig_fourier, number_samples, f_sample, resolucion_frecuencia
        df_datos_medidos, df_fourier, axes_1, axes_2 = utils.parse_contents(content, filename)
        fig_datos, fig_fourier = utils.get_fig(axes_1, type="datos_medidos"), utils.get_fig(axes_2, type="fourier")
        children = utils.valid_content(fig_datos, fig_fourier, filename)
        style = {'display': 'block'}

        number_samples, f_sample = utils.get_signal_properties(df_datos_medidos)
        resolucion_frecuencia = utils.get_frequency_resolution(df_fourier)

    else:
        children = utils.initial_content()
        style = {'display': 'None'}
        
    return children, style

@app.callback(
    Output('numero-muestras', 'children'),          # -> El valor del número muestras
    Output('frecuencia-muestreo', 'children'),      # -> El valor de la frecuencia de muestreo
    Output('resolucion-frecuencia', 'children'),    # -> El valor de la resolución en frecuencia de la transformada de Fourier
    Output('grafica-fourier', 'figure'),          # -> La gráfica de Fourier
    Input('grafica-medidos', 'relayoutData'))       # -> Cómo editamos la barra de abajo de la gráfica
def display_selected_data(relayoutData):
    global number_samples, f_sample, resolucion_frecuencia
    if relayoutData:
        global df_datos_medidos, df_fourier, fig_fourier
        if 'xaxis.range' in relayoutData.keys():
            extremo_izquierdo = relayoutData['xaxis.range'][0]
            extremo_derecho = relayoutData['xaxis.range'][1]
            datos_seleccionados = df_datos_medidos[df_datos_medidos.iloc[:,0] <= extremo_derecho]
            datos_seleccionados = datos_seleccionados[datos_seleccionados.iloc[:,0] >= extremo_izquierdo]
            datos_fourier = utils.get_fft(datos_seleccionados)
            axes_fourier = utils.get_axes(datos_fourier, type="Fourier")
            fig_fourier_temporal = utils.get_fig(axes_fourier, type="Fourier")

            number_samples, f_sample = utils.get_signal_properties(datos_seleccionados)
            resolucion_frecuencia = utils.get_frequency_resolution(datos_fourier)

        if 'xaxis.range[0]' in relayoutData.keys():
                extremo_izquierdo = relayoutData['xaxis.range[0]']
                extremo_derecho = relayoutData['xaxis.range[1]']
                datos_seleccionados = df_datos_medidos[df_datos_medidos.iloc[:,0] <= extremo_derecho]
                datos_seleccionados = datos_seleccionados[datos_seleccionados.iloc[:,0] >= extremo_izquierdo]

                datos_fourier = utils.get_fft(datos_seleccionados)
                axes_fourier = utils.get_axes(datos_fourier, type="Fourier")
                fig_fourier_temporal = utils.get_fig(axes_fourier, type="Fourier")

                number_samples, f_sample = utils.get_signal_properties(datos_seleccionados)
                resolucion_frecuencia = utils.get_frequency_resolution(datos_fourier)

        if 'xaxis.autorange' in relayoutData.keys():
            number_samples, f_sample = utils.get_signal_properties(df_datos_medidos)
            resolucion_frecuencia = utils.get_frequency_resolution(df_fourier)
            fig_fourier_temporal = fig_fourier
    
    else:
        fig_fourier_temporal = fig_fourier
        
    return number_samples, f_sample, resolucion_frecuencia, fig_fourier_temporal

if __name__ == '__main__':
    app.run_server(debug=True)