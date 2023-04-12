import base64
import io

import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from styles import COLORS_STYLE, INITIAL_CONTENT_STYLE, INITIAL_CONTENT_SIM_STYLE

from dash import dcc, html

def get_empty_fig(type="datos_medidos"):
    axes = go.Scatter(x=[], y=[], name = "Medición", marker=dict(color = COLORS_STYLE["plot_color_1"]))
    fig = go.Figure()
    fig.add_trace(axes)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    h = 300
    top_margin = 30

    if type == "datos_medidos":
        fig.update_xaxes(rangeslider_thickness = 0.1)
        fig.update_layout(xaxis=dict(
            rangeslider=dict(visible=True)
            )
        )
        h = 330
        top_margin = 20
    
    fig.update_layout(height=h, width=1100, 
                    #title_text=f"Frecuencia de muestreo: ---",
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    font_color='#8E8F91',
                    margin=dict(l=0, r=0, t=top_margin, b=0))

    return fig

def initial_content_data():
    fig1, fig2 = get_empty_fig(), get_empty_fig("fourier")
    div = html.Div([
        html.H5("Seleccione un archivo en el panel de la izquierda.", style={"color":COLORS_STYLE["text_color"]}),
        dcc.Graph(figure=fig1, id='grafica-medidos'),
        dcc.Graph(figure=fig2, id='grafica-fourier'),
    ], id="output-data-upload", style=INITIAL_CONTENT_STYLE)

    return div

def initial_content_simulation():
    fig1, fig2 = get_empty_fig(), get_empty_fig("fourier")
    div = html.Div([
        html.H5("Seleccione en el panel de la izquierda la señal que desea simular.", style={"color":COLORS_STYLE["text_color"]}),
        dcc.Graph(figure=fig1, id='grafica-señal'),
        dcc.Graph(figure=fig2, id='grafica-fourier-señal'),
    ], id="output-simulation", style=INITIAL_CONTENT_SIM_STYLE)

    return div

def error_content():
    fig1, fig2 = get_empty_fig(), get_empty_fig("fourier")
    div = html.Div([
        html.H5(f'Hubo un error procesando este archivo, por favor asegúrate que es un archivo de tipo .csv o .xls', style={"color":COLORS_STYLE["text_color"]}),
        dcc.Graph(figure=fig1, id='grafica-medidos'),
        dcc.Graph(figure=fig2, id='grafica-fourier'),
    ], id="output-data-upload", style=INITIAL_CONTENT_STYLE)

    return div

def get_fft(df):
    ffty = np.fft.fft(df.iloc[:,1])

    N = len(df)
    f_sample = 1/(df.iloc[1,0] - df.iloc[0,0])
    f_interval = f_sample / N
    hertz = np.arange(N)*f_interval
    hertz = hertz - np.ceil(max(hertz)/2)
    specs = np.fft.fftshift(20*np.log10(ffty))
    specs = [np.linalg.norm(spec) for spec in specs]

    df_fft = pd.DataFrame(data = {"Frecuencia":hertz, "Desibeles":specs})

    return df_fft

def get_dfs(content, filename):
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
    
    raw_file = pd.read_csv(file_str)
    #df_metadata = raw_file.iloc[:13,:]
    df_data = raw_file.iloc[14:,:]
    df_data = df_data.astype(float)

    df_fourier = get_fft(df_data)

    return df_data, df_fourier

def get_axes(df, type="datos_medidos"):
    if type == "datos_medidos":
        axes = go.Scatter(x=df.iloc[:,0], y=df.iloc[:,1], name = "Medición", marker=dict(color = COLORS_STYLE["plot_color_1"]))
    else:
        axes = go.Scatter(x=df.iloc[:,0], y=df.iloc[:,1], name = "Fourier", marker=dict(color = COLORS_STYLE["plot_color_2"]))

    return axes

def parse_contents(content, filename):
    """
    Esta función nos sirve para leer el contenido que estamos seleccionando. Se utiliza en el @callback. 
    Con esta función también estamos decidiendo qué hacemos con el archivo que abrimos. 
    
    
    Por el momento se abre la tabla en la página. Para nada queremos esto. 
    Queremos que esta función sólo genere el archivo y que otras funciones hagan cosas con este archivo.
    """
    df_datos_medidos, df_fourier = get_dfs(content, filename)
    axes_1, axes_2 = get_axes(df_datos_medidos), get_axes(df_fourier, type="fourier")
    
    return df_datos_medidos, df_fourier, axes_1, axes_2

def get_fig(axes, type="datos_medidos", df_datos_medidos=None):
    """
    Función que grafica tanto los datos medidos como la transformada de Fourier de dichos datos.
    """
    fig = go.Figure()
    fig.add_trace(axes)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    h = 300
    top_margin = 30
    
    if type == "datos_medidos":
        fig.update_xaxes(rangeslider_thickness = 0.1)
        fig.update_layout(xaxis=dict(
            rangeslider=dict(visible=True)
            )
        )
        h = 330
        top_margin = 20
    
    fig.update_layout(height=h, width=1100, 
                    #title_text=f"Frecuencia de muestreo: ---",
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    font_color='#8E8F91',
                    margin=dict(l=0, r=0, t=top_margin, b=0))

    return fig

def valid_content(fig1, fig2, filename):
    div = html.Div([
        html.H5(f"Archivo seleccionado: {filename}", style={"color":COLORS_STYLE["text_color"]}),
        dcc.Graph(figure=fig1, id='grafica-medidos'),
        dcc.Graph(figure=fig2, id='grafica-fourier'),
    ])
    return div

def get_signal_properties(df):
    number_samples = len(df)
    f_sample = 1/(df.iloc[1,0] - df.iloc[0,0])
    f_sample = f"{f_sample:1.5} Hz"

    return number_samples, f_sample

def get_frequency_resolution(df):
    frequency_resolution = df.iloc[1,0] - df.iloc[0,0]
    frequency_resolution = f"{frequency_resolution:1.5} Hz"

    return frequency_resolution

