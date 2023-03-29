import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

colors = {"plot_color_1": "#F4D44D",
          "plot_color_2": "#F45060"}

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
        
    
def plot_empty():
        """
        Función que grafica vacío
        """
        fig = make_subplots(rows=2, cols=1)

        fig.update_layout(height=575, width=1100, 
                          plot_bgcolor='rgba(0, 0, 0, 0)',
                          paper_bgcolor='rgba(0, 0, 0, 0)',
                          font_color='#8E8F91')

        return fig, None