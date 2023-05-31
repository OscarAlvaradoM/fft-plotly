import pandas as pd

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html
from dash.exceptions import PreventUpdate

import utils
import utils2
from styles import TABS_STYLE, TABS_STYLE_2, TAB_STYLE, TAB_STYLE_2, SELECTED_STYLE, SELECTED_STYLE_2, INITIAL_CONTENT_ADD_STYLE, INITIAL_CONTENT_OTHER_STYLE, INITIAL_CONTENT_MEASURE_STYLE
from components import sidebar, sidebar2, sidebar3, initial_content_add_signals, initial_content_other_signals, initial_content_measure

f_sample = None
number_samples = None
resolucion_frecuencia = None
datos_medidos_a_mostrar = None
df_datos_medidos, df_fourier = None, None
fig_datos_medidos, fig_fourier = utils.get_empty_fig(), utils.get_empty_fig(type="Fourier")

df_simulations, df_fourier_simulations = None, None
fig_simulation, fig_fourier_simulation = utils.get_empty_fig(), utils.get_empty_fig(type="Fourier")

df_simulations_other_signals, df_fourier_simulations_other_signals = None, None
fig_simulation_other_signals, fig_fourier_simulation_other_signals = utils.get_empty_fig(), utils.get_empty_fig(type="Fourier")

content_measure = html.Div(id="output-data-upload", children=initial_content_measure, style=INITIAL_CONTENT_MEASURE_STYLE)
content_add_signals = html.Div(id="output-add-signals", children=initial_content_add_signals, style=INITIAL_CONTENT_ADD_STYLE)
content_other_signals = html.Div(id="output-other-signals", children=initial_content_other_signals, style=INITIAL_CONTENT_OTHER_STYLE)

# Con esto inicializamos la aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Aquí definimos la plantilla inicial. Habría que colocar todos los elementos que queremos de principio y serán los que se irán actualizando.
app.layout = html.Div([
    dcc.Tabs(
        [
        dcc.Tab(label='Aprendiendo con la FFT', children=
            [
            dcc.Tabs([
                dcc.Tab(label='Suma de señales', children=
                    [
                        sidebar2, content_add_signals
                    ], 
                style=TAB_STYLE_2, selected_style=SELECTED_STYLE_2),

                dcc.Tab(label='Otras señales', children=
                    [
                        sidebar3, content_other_signals
                    ],
                style=TAB_STYLE_2, selected_style=SELECTED_STYLE_2)
            ], style=TABS_STYLE_2)
            ], 
        style=TAB_STYLE, selected_style=SELECTED_STYLE),

        dcc.Tab(label='Experimentando con la FFT', children=
            [
                sidebar, content_measure
            ], 
        style=TAB_STYLE, selected_style=SELECTED_STYLE)
        ], 
    style=TABS_STYLE)
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
    Output('grafica-fourier', 'figure'),            # -> La gráfica de Fourier
    Input('grafica-medidos', 'relayoutData'))       # -> Cómo editamos la barra de abajo de la gráfica
def display_selected_data(relayout_data):
    global number_samples, f_sample, resolucion_frecuencia
    if relayout_data:
        global df_datos_medidos, df_fourier, fig_fourier
        if 'xaxis.range' in relayout_data.keys():
            extremo_izquierdo = relayout_data['xaxis.range'][0]
            extremo_derecho = relayout_data['xaxis.range'][1]
            datos_seleccionados = df_datos_medidos[df_datos_medidos.iloc[:,0] <= extremo_derecho]
            datos_seleccionados = datos_seleccionados[datos_seleccionados.iloc[:,0] >= extremo_izquierdo]
            datos_fourier = utils.get_fft(datos_seleccionados)
            axes_fourier = utils.get_axes(datos_fourier, type="Fourier")
            fig_fourier_temporal = utils.get_fig(axes_fourier, type="Fourier")

            number_samples, f_sample = utils.get_signal_properties(datos_seleccionados)
            resolucion_frecuencia = utils.get_frequency_resolution(datos_fourier)

        if 'xaxis.range[0]' in relayout_data.keys():
                extremo_izquierdo = relayout_data['xaxis.range[0]']
                extremo_derecho = relayout_data['xaxis.range[1]']
                datos_seleccionados = df_datos_medidos[df_datos_medidos.iloc[:,0] <= extremo_derecho]
                datos_seleccionados = datos_seleccionados[datos_seleccionados.iloc[:,0] >= extremo_izquierdo]

                datos_fourier = utils.get_fft(datos_seleccionados)
                axes_fourier = utils.get_axes(datos_fourier, type="Fourier")
                fig_fourier_temporal = utils.get_fig(axes_fourier, type="Fourier")

                number_samples, f_sample = utils.get_signal_properties(datos_seleccionados)
                resolucion_frecuencia = utils.get_frequency_resolution(datos_fourier)

        if 'xaxis.autorange' in relayout_data.keys():
            number_samples, f_sample = utils.get_signal_properties(df_datos_medidos)
            resolucion_frecuencia = utils.get_frequency_resolution(df_fourier)
            fig_fourier_temporal = fig_fourier
    
    else:
        fig_fourier_temporal = fig_fourier
        
    return number_samples, f_sample, resolucion_frecuencia, fig_fourier_temporal

# Para sumar señales simuladas
@app.callback(
    # Para mostrar las simulaciones
    Output("output-add-signals", "children"),
    # Abrimos o cerramos la ventana emergente
    Output("modal-signal-adding", "is_open"),
    # Reiniciamos nuestros botones
    Output("button-add-signal", "n_clicks"),
    Output("button-reset-signal", "n_clicks"),
    Output("ok-button", "n_clicks"),
    Output("cancel-button", "n_clicks"),
    # Reiniciamos los valores a guardar
    Output("frecuencia", "value"),
    Output("amplitud", "value"),
    # Para mostrar u ocultar el botón de reinicio
    Output("button-reset-signal", "style"),
    # Para cambiar la leyenda que muestra el botón
    Output("button-add-signal", "children"),

    # Aquí los valores de entrada de los botones
    Input("button-add-signal", "n_clicks"),
    Input("ok-button", "n_clicks"),
    Input("cancel-button", "n_clicks"),
    # El botón de reinicio
    Input("button-reset-signal", "n_clicks"),
    # Aquí los valores de la nueva onda a agregar
    Input("frecuencia", "value"),
    Input("amplitud", "value"),

    # Estado de la ventana emergente
    State("modal-signal-adding", "is_open"),
)
def open_modal_add_signals(add_button, ok_button, cancel_button, reset_button, 
               frecuencia, amplitud,
               is_open):
    global df_simulations, df_fourier_simulations, fig_simulation, fig_fourier_simulation
    ventana_visible = False
    reset_button_style = {'display': 'None'}
    button_legend = "Sumar señales"

    # Para habilitar o deshabilitar los componentes de tipo de onda y de resolución
    if isinstance(df_simulations, type(pd.DataFrame())):
        children = utils2.valid_signal_content(fig_simulation, fig_fourier_simulation)
        reset_button_style = {'display': 'block'}
    else:
        children = utils2.initial_content_simulation()
        button_legend = "Sumar señales"

    # Si está abierta, sólo puede aceptar lo que tengo o cerrar la ventana y cancelar.
    if is_open:
        if cancel_button:
            print("Cancelo")
            ventana_visible = False

        elif ok_button:
            print("Ok")
            if frecuencia == None or amplitud == None:
                print("Te falta llenar algunos campos") 
                ventana_visible = True
                ok_button = None
                raise PreventUpdate
            else:
                ventana_visible = False
                # Si el df de las simulaciones está vacío, creamos una simulación
                if not isinstance(df_simulations, type(pd.DataFrame())):
                    df_simulations, df_fourier_simulations, axes_signal, axes_fourier_signal = utils2.create_signal_data(amplitud, frecuencia)
                    fig_simulation, fig_fourier_simulation = utils.get_fig(axes_signal, type="datos_medidos"), utils.get_fig(axes_fourier_signal, type="fourier")
                    children = utils2.valid_signal_content(fig_simulation, fig_fourier_simulation)
                else:
                    df_simulations, df_fourier_simulations, axes_signal, axes_fourier_signal = utils2.add_signal_data( 
                                                                                                amplitud, frecuencia,
                                                                                                df_simulations)
                    fig_simulation, fig_fourier_simulation = utils.get_fig(axes_signal, type="datos_medidos"), utils.get_fig(axes_fourier_signal, type="fourier")
                    children = utils2.valid_signal_content(fig_simulation, fig_fourier_simulation)
                reset_button_style = {'display': 'block'}
                button_legend = "Agregar señal"
        
        else:
            ventana_visible = True
            raise PreventUpdate

    # Si está cerrada, sólo puedo abrirla o borrar lo que ya tenía.
    else:
        if add_button:
            print("Abro la ventana")
            ventana_visible = True
        
        elif reset_button:
            print("Reinicio")
            ventana_visible = False
            df_simulations = None
            children = utils2.initial_content_simulation()
            reset_button_style = {'display': 'None'}
            button_legend = "Sumar señales"
        
        else:
            raise PreventUpdate
    return children, ventana_visible, None, None, None, None, None, None, reset_button_style, button_legend

# Para agregar otras señales simuladas
@app.callback(
    # Para mostrar las simulaciones
    Output("output-other-signals", "children"),
    # Abrimos o cerramos la ventana emergente
    Output("modal-other-signals", "is_open"),
    # Reiniciamos nuestros botones
    Output("button-other-signals", "n_clicks"),
    Output("button-reset-other-signals", "n_clicks"),
    Output("ok-button-other-signals", "n_clicks"),
    Output("cancel-button-other-signals", "n_clicks"),
    # Reiniciamos los valores a guardar
    Output("tipo-onda", "value"),
    Output("frecuencia-other-signals", "value"),
    Output("amplitud-other-signals", "value"),
    # Para mostrar u ocultar el botón de reinicio
    Output("button-reset-other-signals", "style"),
    
    # Aquí los valores de entrada de los botones
    Input("button-other-signals", "n_clicks"),
    Input("ok-button-other-signals", "n_clicks"),
    Input("cancel-button-other-signals", "n_clicks"),
    # El botón de reinicio
    Input("button-reset-other-signals", "n_clicks"),
    # Aquí los valores de la nueva onda a agregar
    Input("tipo-onda", "value"),
    Input("frecuencia-other-signals", "value"),
    Input("amplitud-other-signals", "value"),

     # Estado de la ventana emergente
    State("modal-other-signals", "is_open"),
)
def open_modal_other_signals(add_button_other_signals, ok_button_other_signals, cancel_button_other_signals, reset_button_other_signals, 
               tipo_onda_other_signals, frecuencia_other_signals, amplitud_other_signals,
               is_open_other_signals):
    global df_simulations_other_signals, df_fourier_simulations_other_signals, fig_simulation_other_signals, fig_fourier_simulation_other_signals
    ventana_visible = False
    reset_button_style = {'display': 'None'}

    # Para habilitar o deshabilitar los componentes de tipo de onda y de resolución
    if isinstance(df_simulations_other_signals, type(pd.DataFrame())):
        tipo_onda_other_signals = df_simulations_other_signals.columns[-1]
        children = utils2.valid_signal_content(fig_simulation_other_signals, fig_fourier_simulation_other_signals)
        reset_button_style = {'display': 'block'}
    
    else:
        children = utils2.initial_content_simulation()

    # Si está abierta, sólo puede aceptar lo que tengo o cerrar la ventana y cancelar.
    if is_open_other_signals:
        if cancel_button_other_signals:
            print("Cancelo")
            ventana_visible = False

        elif ok_button_other_signals:
            print("Ok")
            if tipo_onda_other_signals == None or frecuencia_other_signals == None or amplitud_other_signals == None:
                print("Te falta llenar algunos campos") 
                ventana_visible = True
                ok_button_other_signals = None
                tipo_onda_other_signals = None
                raise PreventUpdate
            else:
                ventana_visible = False
                # Si el df de las simulaciones está vacío, creamos una simulación
                df_simulations_other_signals, df_fourier_simulations_other_signals, axes_signal, axes_fourier_signal = utils2.create_signal_data(amplitud_other_signals, frecuencia_other_signals, 
                                                                                                                         tipo_onda_other_signals)
                fig_simulation_other_signals, fig_fourier_simulation_other_signals = utils.get_fig(axes_signal, type="datos_medidos"), utils.get_fig(axes_fourier_signal, type="fourier")
                children = utils2.valid_signal_content(fig_simulation_other_signals, fig_fourier_simulation_other_signals)
                reset_button_style = {'display': 'block'}
        
        else:
            ventana_visible = True
            tipo_onda_other_signals = None
            raise PreventUpdate

    # Si está cerrada, sólo puedo abrirla o borrar lo que ya tenía.
    else:
        if add_button_other_signals:
            print("Abro la ventana")
            ventana_visible = True
        
        elif reset_button_other_signals:
            print("Reinicio")
            tipo_onda_other_signals = None
            ventana_visible = False
            df_simulations_other_signals = None
            children = utils2.initial_content_simulation()
            reset_button_style = {'display': 'None'}
        
        else:
            tipo_onda_other_signals = None
            raise PreventUpdate
    return children, ventana_visible, None, None, None, None, tipo_onda_other_signals, None, None, reset_button_style


@app.callback(
    Output("modal-spectrogram", "is_open"),         # -> Ventana emergente con espectrograma
    Output('button-spectrogram', 'n_clicks'),       # -> Para reiniciar el botón para mostrar el espectrograma
    Output('grafica-modal-spectrogram', 'figure'),  # -> La gráfica del espectrograma
    Input('button-spectrogram', 'n_clicks'),        # -> El botón para mostrar el espectrograma
)
def display_selected_data(n_clicks):
    global df_datos_medidos
    if n_clicks:
        return True, None, utils.get_spectrogram(df_datos_medidos)
    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)