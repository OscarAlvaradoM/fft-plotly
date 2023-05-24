import base64
import io

import numpy as np
import pandas as pd

import plotly.graph_objects as go
#import matplotlib.pyplot as plt

from styles import COLORS_STYLE
from components import initial_content_measure, initial_error_content_measure

from dash import dcc, html

def get_empty_fig(type="datos_medidos"):
    axes = go.Scatter(x=[], y=[], name = "Medición", marker=dict(color = COLORS_STYLE["plot_color_1"]))
    fig = go.Figure()
    fig.add_trace(axes)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    h = 280
    top_margin = 30

    if type == "datos_medidos":
        fig.update_xaxes(rangeslider_thickness = 0.1)
        fig.update_layout(xaxis=dict(
            rangeslider=dict(visible=True)
            )
        )
        h = 310
        top_margin = 20
    
    fig.update_layout(height=h, width=1100, 
                    #title_text=f"Frecuencia de muestreo: ---",
                    plot_bgcolor='rgba(0, 0, 0, 0)',
                    paper_bgcolor='rgba(0, 0, 0, 0)',
                    font_color='#8E8F91',
                    margin=dict(l=0, r=0, t=top_margin, b=0))

    return fig

def initial_content_data():
    div = html.Div(initial_content_measure)

    return div

def error_content():
    div = html.Div(initial_error_content_measure)

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
    h = 280
    top_margin = 30
    
    if type == "datos_medidos":
        fig.update_xaxes(rangeslider_thickness = 0.1)
        fig.update_layout(xaxis=dict(
            rangeslider=dict(visible=True)
            )
        )
        h = 310
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

def get_spectrogram(df_signal):
    if isinstance(df_signal, type(pd.DataFrame())):
        # print(df_signal.iloc[:, -1].values)
        # fig, ax = plt.subplots(figsize = (10,10))
        # ax.specgram(df_signal.iloc[:, -1].values, Fs=6, cmap="rainbow")
        # ax.set_title('Spectrogram Using matplotlib.pyplot.specgram() Method')
        # ax.set_xlabel("DATA")
        # ax.set_ylabel("TIME")

        trace1 = {
        "type": "heatmap", 
        "x": df_signal.iloc[:,0].values,
        "y": np.sort(np.random.rand(len(df_signal))),
        "z": df_signal.iloc[:,1].values,
        "colorscale": "Jet"}

        data = go.Heatmap(z=trace1["z"], x=trace1["x"], y=trace1["y"], colorscale=trace1["colorscale"])
        layout = {
        "title": {"text": "Espectrograma de los datos medidos."}, 
        "xaxis": {"title": {"text": "Tiempo"}}, 
        "yaxis": {"title": {"text": "Frecuencia"}},
        "width": 650,
        "height": 650,
        }
        fig = go.Figure(data=data, layout=layout)

        # fig = go.Figure(data=go.Heatmap(
        #             z=[[1, 20, 30],
        #               [20, 1, 60],
        #               [30, 60, 1]],
        #             text=[['one', 'twenty', 'thirty'],
        #                   ['twenty', 'one', 'sixty'],
        #                   ['thirty', 'sixty', 'one']],
        #             texttemplate="%{text}",
        #             textfont={"size":20}))

        return fig
    else:
        return None