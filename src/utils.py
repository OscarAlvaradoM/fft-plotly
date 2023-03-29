import base64
import io

import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from styles import COLORS_STYLE, SIDEBAR_STYLE, CONTENT_STYLE, UPLOAD_STYLE, INITIAL_CONTENT_STYLE

from dash import dcc, html

#colors = {"plot_color_1": "#F4D44D",
#          "plot_color_2": "#F45060"}

class Onda():
    def __init__(self, file):
        """
        Constructor del objeto Onda, que alberga datos de un documento de mediciones de osciloscopio. Separa entre datos y metadatos."""
        raw_file = pd.read_csv(file)
        self.metadata = raw_file.iloc[:13,:]
        self.data = raw_file.iloc[14:,:]
        self.data = self.data.astype(float)
        self.f_sample = 1/(self.data.iloc[1,0] - self.data.iloc[0,0])
            
    def plot_fourier(self, numero_de_muestras=None):
        """
        Función que grafica tanto los datos medidos como la transformada de Fourier de dichos datos.
        """
        data = self.data
        f_sample = self.f_sample
        
        fig = make_subplots(rows=2, cols=1)

        fig.add_trace(go.Scatter(x=data.iloc[:,0], y=data.iloc[:,1], name = "Medición", marker=dict(color = colors["plot_color_1"])),row=1, col=1)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        ffty = np.fft.fft(data.iloc[:,1])

        N = len(data)
        f_interval = f_sample / N
        hertz = np.arange(N)*f_interval
        hertz = hertz - np.ceil(max(hertz)/2)
        specs = np.fft.fftshift(20*np.log10(ffty))
        specs = [np.linalg.norm(spec) for spec in specs]
        fig.add_trace(go.Scatter(x=hertz, y=specs, name = "Fourier", marker=dict(color = colors["plot_color_2"])), row=2, col=1)

        fig.update_layout(height=600, width=1100, 
                          title_text=f"Frecuencia de muestreo: {f_sample:1.5} hz",
                          plot_bgcolor='rgba(0, 0, 0, 0)',
                          paper_bgcolor='rgba(0, 0, 0, 0)',
                          font_color='#8E8F91')

        fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.46,
        xanchor="right",
        x=1),
        margin=dict(l=0, r=0, t=30, b=0))

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        return fig, N
    
def plot_content(file_str=None, numero_muestras=None):
    if file_str == None:
        fig, numero_muestras = plot_empty()
    else:
        onda = Onda(file_str)
        fig, numero_muestras = onda.plot_fourier(numero_muestras)
    return fig, numero_muestras
        

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

def get_empty_axes():
    axes_1 = go.Scatter(x=[], y=[], name = "Medición", marker=dict(color = COLORS_STYLE["plot_color_1"]))
    axes_2 = go.Scatter(x=[], y=[], name = "Fourier", marker=dict(color = COLORS_STYLE["plot_color_2"]))

    return axes_1, axes_2

def get_axes(df_1, df_2):
     axes_1 = go.Scatter(x=df_1.iloc[:,0], y=df_1.iloc[:,1], name = "Medición", marker=dict(color = COLORS_STYLE["plot_color_1"]))
     axes_2 = go.Scatter(x=df_2.iloc[:,0], y=df_2.iloc[:,1], name = "Fourier", marker=dict(color = COLORS_STYLE["plot_color_2"]))

     return axes_1, axes_2

def get_fig(axes_1, axes_2, df_1):
    """
    Función que grafica tanto los datos medidos como la transformada de Fourier de dichos datos.
    """
    if not isinstance(df_1, type(None)):
        f_sample = 1/(df_1.iloc[1,0] - df_1.iloc[0,0])
        number_samples = len(df_1)
    else:
        f_sample = 0.0
        number_samples = 0
    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(axes_1,row=1, col=1)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.add_trace(axes_2, row=2, col=1)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.update_layout(height=600, width=1100, 
                        title_text=f"Frecuencia de muestreo: {f_sample:1.5} hz",
                        plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)',
                        font_color='#8E8F91')

    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=0.46,
    xanchor="right",
    x=1),
    margin=dict(l=0, r=0, t=30, b=0))

    return fig, number_samples

def initial_content():
    axes_1, axes_2 = get_empty_axes()
    fig, _ = get_fig(axes_1, axes_2, None)
    div = html.Div([
        html.H5("Seleccione un archivo en el panel de la izquierda.", style={"color":COLORS_STYLE["text_color"]}),
        dcc.Graph(figure=fig, id='graficas'),
    ], id="output-data-upload", style=INITIAL_CONTENT_STYLE)

    return div

def valid_content(fig, filename):
    div = html.Div([
        html.H5(f"Archivo seleccionado: {filename}", style={"color":COLORS_STYLE["text_color"]}),
        dcc.Graph(figure=fig, id='graficas'),
    ])
    return div

def error_content():
    fig = get_fig(get_empty_axes())
    div = html.Div([
        html.H5(f'Hubo un error procesando este archivo, por favor asegúrate que es un archivo de tipo .csv o .xls', style={"color":COLORS_STYLE["text_color"]}),
        dcc.Graph(figure=fig, id='graficas'),
    ], id="output-data-upload", style=INITIAL_CONTENT_STYLE)

    return div

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
    df_metadata = raw_file.iloc[:13,:]
    df_data = raw_file.iloc[14:,:]
    df_data = df_data.astype(float)

    df_fourier = get_fft(df_data)

    return df_data, df_fourier

def parse_contents(content, filename):
    """
    Esta función nos sirve para leer el contenido que estamos seleccionando. Se utiliza en el @callback. 
    Con esta función también estamos decidiendo qué hacemos con el archivo que abrimos. 
    
    
    Por el momento se abre la tabla en la página. Para nada queremos esto. 
    Queremos que esta función sólo genere el archivo y que otras funciones hagan cosas con este archivo.
    """
    df_datos_medidos, df_fourier = get_dfs(content, filename)
    axes_1, axes_2 = get_axes(df_datos_medidos, df_fourier)
    
    return df_datos_medidos, df_fourier, axes_1, axes_2

def change_number_samples(df_1, df_2, number_samples):
    df_1 = df_1.iloc[:number_samples,:]
    df_2 = get_fft(df_1)

    return df_1, df_2
