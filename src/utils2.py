import numpy as np
import pandas as pd

from scipy import signal

import plotly.graph_objects as go

from dash import dcc, html
from styles import COLORS_STYLE, CENTERED_CONTENT_STYLE

from utils import get_fft
from components import initial_content_sim


def initial_content_simulation():
    div = html.Div(initial_content_sim)

    return div

def reset_content_simulation():
    div = html.Div([
        html.H5("Vuelva a presionar 'Agregar señal' en el panel de la izquierda para configurar señal a simular.", style={"color":COLORS_STYLE["text_color"]}),
        html.H1("Simulación de datos.", style=CENTERED_CONTENT_STYLE),
    ])

    return div

# ------------------ Acá vienen las funciones de las señales simuladas ---------------------
def get_dfs_signal(signal_type="Sinusoidal", amplitude=1, number_periods=6, resolution=3_000, tiempo_muestra=0.0032):
    print(signal_type, amplitude, number_periods, resolution, tiempo_muestra)
    t = np.linspace(-tiempo_muestra/2, tiempo_muestra/2, resolution)
    frequency = number_periods / tiempo_muestra
    w = 2*np.pi*frequency
    A = amplitude / 2

    if signal_type == "Sinusoidal":
        y = A*np.sin(w*t)

    elif signal_type == 'Cuadrada':
        y = A*signal.square(w* t, duty=(np.sin(w*t) + 1)/2)

    elif signal_type == 'Triangular':
        y = A*signal.sawtooth(w*t,0.5)

    elif signal_type == 'Sierra':
        y = A*signal.sawtooth(w*t)

    df_signal = pd.DataFrame({"tiempo":t, f"{signal_type}":y})
    df_fourier = get_fft(df_signal)

    return df_signal, df_fourier

def get_axes_sim(df, type="datos_simulados"):
    if type == "datos_simulados":
        axes = go.Scatter(x=df.iloc[:,0], y=df.iloc[:,-1], name = "Simulación", marker=dict(color = COLORS_STYLE["plot_color_1"]))
    else:
        axes = go.Scatter(x=df.iloc[:,0], y=df.iloc[:,-1], name = "Fourier", marker=dict(color = COLORS_STYLE["plot_color_2"]))

    return axes

def create_signal_data(signal_type="Sinusoidal", amplitude=1, number_periods=6, resolution=3_000, tiempo_muestra=0.0032):
    df_signal, df_fourier_signal = get_dfs_signal(signal_type, amplitude, number_periods, resolution, tiempo_muestra)
    axes_signal, axes_fourier_signal = get_axes_sim(df_signal), get_axes_sim(df_fourier_signal, type="fourier")
    
    return df_signal, df_fourier_signal, axes_signal, axes_fourier_signal

def valid_signal_content(fig1, fig2, signal_type):
    div = html.Div([
        html.H5("Presione 'Agregar señal' en el panel de la izquierda para sumar señales simuladas a esta señal.", style={"color":COLORS_STYLE["text_color"]}),
        html.H5(f"Tipo de ondas: {signal_type}", style={"color":COLORS_STYLE["text_color"]}),
        dcc.Graph(figure=fig1, id='grafica-signal'),
        dcc.Graph(figure=fig2, id='grafica-signal-fourier'),
    ])
    return div

# Para generar el df de las señales sumadas
def get_added_dfs_signal(signal_type, amplitude, number_periods, resolution, tiempo_muestra, df_simulations):
    df_new_signal, _ = get_dfs_signal(signal_type, amplitude, number_periods, resolution, tiempo_muestra)
    df_added = df_simulations.iloc[:, -1] + df_new_signal.iloc[:, -1]
    df_added = pd.concat([df_simulations, df_new_signal.iloc[:, -1], df_added], axis=1)

    df_added_fourier_signal = get_fft(df_added.iloc[:, [0, -1]])

    return df_added, df_added_fourier_signal

# Para agregar una señal
def add_signal_data(signal_type, amplitude, number_periods, resolution, df_simulations, tiempo_muestra=0.0032):
    """
    Función para sumar una señal a otra u otras señales previamente generadas.
    """
    df_signal, df_fourier_signal = get_added_dfs_signal(signal_type, amplitude, number_periods, resolution, tiempo_muestra, df_simulations)
    axes_signal, axes_fourier_signal = get_axes_sim(df_signal), get_axes_sim(df_fourier_signal, type="fourier")
    
    return df_signal, df_fourier_signal, axes_signal, axes_fourier_signal