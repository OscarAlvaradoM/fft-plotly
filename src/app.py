import pandas as pd

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html
from dash.exceptions import PreventUpdate

import utils
import utils2
from styles import TABS_STYLE, TAB_STYLE, SELECTED_STYLE, INITIAL_CONTENT_SIM_STYLE, INITIAL_CONTENT_MEASURE_STYLE
from components import sidebar, sidebar2, initial_content_sim, initial_content_measure

f_sample = None
number_samples = None
resolucion_frecuencia = None
datos_medidos_a_mostrar = None
df_datos_medidos, df_fourier = None, None
fig_datos_medidos, fig_fourier = utils.get_empty_fig(), utils.get_empty_fig(type="Fourier")
grafica1 = dcc.Graph(figure=fig_datos_medidos, id='grafica-medidos')
grafica2 = dcc.Graph(figure=fig_fourier, id='grafica-fourier')

df_simulations, df_fourier_simulations = None, None
fig_simulation, fig_fourier_simulation = utils.get_empty_fig(), utils.get_empty_fig(type="Fourier")

content_measure = html.Div(id="output-data-upload", children=initial_content_measure, style=INITIAL_CONTENT_MEASURE_STYLE)
content_sim = html.Div(id="output-simulation", children=initial_content_sim, style=INITIAL_CONTENT_SIM_STYLE)

# Con esto inicializamos la aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Aquí definimos la plantilla inicial. Habría que colocar todos los elementos que queremos de principio y serán los que se irán actualizando.
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Lectura de datos', children=
        [
                sidebar, content_measure
        ], 
        style=TAB_STYLE, selected_style=SELECTED_STYLE),

        dcc.Tab(label='Simulación de datos', children=
        [
            sidebar2, content_sim
        ], 
        style=TAB_STYLE, selected_style=SELECTED_STYLE)
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
    # Para mostrar las simulaciones
    Output("output-simulation", "children"),
    # Abrimos o cerramos la ventana emergente
    Output("modal-centered", "is_open"),
    # Reiniciamos nuestros botones
    Output("button-add-signal", "n_clicks"),
    Output("button-reset-signal", "n_clicks"),
    Output("ok-button", "n_clicks"),
    Output("cancel-button", "n_clicks"),
    # Reiniciamos los valores a guardar
    Output("tipo-onda", "value"),
    Output("numero-periodos", "value"),
    Output("amplitud", "value"),
    Output("resolucion", "value"),
    # Para bloquear el estado de ciertos componentes
    Output("tipo-onda", "disabled"),
    Output("resolucion", "disabled"),
    # Para mostrar u ocultar el botón de reinicio
    Output("button-reset-signal", "style"),
    # Aquí los valores de entrada de los botones
    Input("button-add-signal", "n_clicks"),
    Input("ok-button", "n_clicks"),
    Input("cancel-button", "n_clicks"),
    # El botón de reinicio
    Input("button-reset-signal", "n_clicks"),
    # Aquí los valores de la nueva onda a agregar
    Input("tipo-onda", "value"),
    Input("numero-periodos", "value"),
    Input("amplitud", "value"),
    Input("resolucion", "value"),
    # Estado de la ventana emergente
    State("modal-centered", "is_open"),
)
def open_modal(add_button, ok_button, cancel_button, reset_button, 
               tipo_onda, numero_periodos, amplitud, resolucion, 
               is_open):
    global df_simulations, df_fourier_simulations, fig_simulation, fig_fourier_simulation
    ventana_visible = False
    tipo_onda_disabled = False
    resolucion_disabled = False
    reset_button_style = {'display': 'None'}

    # Para habilitar o deshabilitar los componentes de tipo de onda y de resolución
    if isinstance(df_simulations, type(pd.DataFrame())):
        tipo_onda_disabled = True
        resolucion_disabled = True
        resolucion = len(df_simulations)
        tipo_onda = df_simulations.columns[-1]
        children = utils2.valid_signal_content(fig_simulation, fig_fourier_simulation, tipo_onda)
        reset_button_style = {'display': 'block'}
    
    else:
        children = utils2.initial_content_simulation()

    # Si está abierta, sólo puede aceptar lo que tengo o cerrar la ventana y cancelar.
    if is_open:
        if cancel_button:
            print("Cancelo")
            ventana_visible = False

        elif ok_button:
            print("Ok")
            if tipo_onda == None or numero_periodos == None or amplitud == None or resolucion == None:
                print("Te falta llenar algunos campos") 
                ventana_visible = True
                ok_button = None
                tipo_onda = None
                resolucion = None
                raise PreventUpdate
            else:
                ventana_visible = False
                # Si el df de las simulaciones está vacío, creamos una simulación
                if not isinstance(df_simulations, type(pd.DataFrame())):
                    df_simulations, df_fourier_simulations, axes_signal, axes_fourier_signal = utils2.create_signal_data(tipo_onda, amplitud, numero_periodos, resolucion)
                    fig_simulation, fig_fourier_simulation = utils.get_fig(axes_signal, type="datos_medidos"), utils.get_fig(axes_fourier_signal, type="fourier")
                    children = utils2.valid_signal_content(fig_simulation, fig_fourier_simulation, tipo_onda)
                else:
                    df_simulations, df_fourier_simulations, axes_signal, axes_fourier_signal = utils2.add_signal_data(tipo_onda, 
                                                                                                amplitud, numero_periodos, resolucion,
                                                                                                df_simulations)
                    fig_simulation, fig_fourier_simulation = utils.get_fig(axes_signal, type="datos_medidos"), utils.get_fig(axes_fourier_signal, type="fourier")
                    children = utils2.valid_signal_content(fig_simulation, fig_fourier_simulation, tipo_onda)
                reset_button_style = {'display': 'block'}
        
        else:
            ventana_visible = True
            tipo_onda = None
            resolucion = None
            raise PreventUpdate

    # Si está cerrada, sólo puedo abrirla o borrar lo que ya tenía.
    else:
        if add_button:
            print("Abro la ventana")
            ventana_visible = True
        
        elif reset_button:
            print("Reinicio")
            tipo_onda = None
            resolucion = None
            ventana_visible = False
            tipo_onda_disabled = False
            resolucion_disabled = False
            df_simulations = None
            children = utils2.initial_content_simulation()
            reset_button_style = {'display': 'None'}
        
        else:
            tipo_onda = None
            resolucion = None
            raise PreventUpdate
    #print("Children: ",  children)
    return children, ventana_visible, None, None, None, None, tipo_onda, None, None, resolucion, tipo_onda_disabled, resolucion_disabled, reset_button_style

if __name__ == '__main__':
    app.run_server(debug=True)