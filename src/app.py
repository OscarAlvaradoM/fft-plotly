import plotly.graph_objects as go

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html
from dash.exceptions import PreventUpdate

import utils
from styles import COLORS_STYLE, TABS_STYLE, TAB_STYLE, SELECTED_STYLE, INITIAL_CONTENT_SIM_STYLE
from components import sidebar, sidebar2

f_sample = None
number_samples = None
resolucion_frecuencia = None
datos_medidos_a_mostrar = None
df_datos_medidos, df_fourier = None, None
fig_datos_medidos, fig_fourier = utils.get_empty_fig(), utils.get_empty_fig(type="Fourier")

# Con esto inicializamos la aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Aquí definimos la plantilla inicial. Habría que colocar todos los elementos que queremos de principio y serán los que se irán actualizando.
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Lectura de datos', children=
        [
                sidebar, utils.initial_content_data()
        ], style=TAB_STYLE, selected_style=SELECTED_STYLE),
        dcc.Tab(label='Simulación de datos', children=
        [
            sidebar2, utils.initial_content_simulation()
        ], style=TAB_STYLE, selected_style=SELECTED_STYLE)
    ], style=TABS_STYLE)
])

# ------------------------------------------ Callbacks -----------------------------------------------------------------------
# Cuando se invocan datos medidos desde un CSV o un excel
@app.callback(Output('output-data-upload', 'children'), # -> Es el componente que estoy editando desde acá
              Output('propiedades1', 'style'),              # -> El estado de visibilidad del número de muestras
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
        children = utils.initial_content_data()
        style = {'display': 'None'}
        
    return children, style

# Cuando se selecciona una sección específica de la gráfica amarilla.
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

# Para agregar señales simuladas
@app.callback(
    # Abrimos o cerramos la ventana emergente
    Output("modal-centered", "is_open"),
    # Reiniciamos nuestros botones
    Output("button-add-signal", "n_clicks"),
    Output("ok-button", "n_clicks"),
    Output("cancel-button", "n_clicks"),
    # Reiniciamos lso valores a guardar
    Output("tipo-onda", "value"),
    Output("numero-periodos", "value"),
    Output("amplitud", "value"),
    Output("resolucion", "value"),
    # Aquí los valores de entrada de los botones
    Input("button-add-signal", "n_clicks"),
    Input("ok-button", "n_clicks"),
    Input("cancel-button", "n_clicks"),
    # Aquí los valores de la nueva onda a agregar
    Input("tipo-onda", "value"),
    Input("numero-periodos", "value"),
    Input("amplitud", "value"),
    Input("resolucion", "value"),
    # Estado de la ventana emergente
    State("modal-centered", "is_open"),
)
def open_modal(add_button, ok_button, cancel_button,
               tipo_onda, numero_periodos, amplitud, resolucion, is_open):
    
    ventana_visible = False


    # Si está abierta, sólo puede aceptar lo que tengo o cerrar la ventana y cancelar.
    if is_open:
        if cancel_button:
            print("Cancelo")
            cancel_button = None
            ventana_visible = False

        elif ok_button:
            print("Ok")
            ok_button = None
            if tipo_onda == None or numero_periodos == None or amplitud == None or resolucion == None:
                print("Te falta llenar algunos campos") 
                ventana_visible = True
                raise PreventUpdate
            else:
                ventana_visible = False
                print("Guardamos los datos")
                print("Tipo de onda: ", tipo_onda)
                print("Número de periodos: ", numero_periodos)
                print("Amplitud: ", amplitud)
                print("Resolución: ", resolucion)
        
        else:
            ventana_visible = True
            raise PreventUpdate

    # Si está cerrada, sólo puedo abrirla.
    else:
        if add_button:
            print("Abro la ventana")
            add_button = None
            ventana_visible = True
        else:
            raise PreventUpdate
    return ventana_visible, add_button, ok_button, cancel_button, None, None, None, None

if __name__ == '__main__':
    app.run_server(debug=True)