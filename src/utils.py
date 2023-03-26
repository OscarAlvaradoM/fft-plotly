import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Onda():
    def __init__(self, file):
        raw_file = pd.read_csv(file)
        self.metadata = raw_file.iloc[:13,:]
        self.data = raw_file.iloc[14:,:]
        self.data = self.data.astype(float)
            
    def plot_fourier(self, f_sample=0.001):

        data = self.data
        fig = make_subplots(rows=2, cols=1)

        fig.add_trace(go.Scatter(x=data.iloc[:,0], y=data.iloc[:,1], name = "Medición", marker=dict(color = "#F45060")),row=1, col=1)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        ffty = np.fft.fft(data.iloc[:,1])

        N = len(data)
        f_interval = f_sample / N
        hertz = np.arange(N)*f_interval
        hertz = hertz - np.ceil(max(hertz)/2)
        specs = np.fft.fftshift(20*np.log10(ffty))
        specs = [np.linalg.norm(spec) for spec in specs]
        fig.add_trace(go.Scatter(x=hertz, y=specs, name = "Fourier", marker=dict(color = "#2BC093")), row=2, col=1)

        fig.update_layout(height=600, width=1100, 
                          #title_text=f"Resolución: {resolution} s<br>Frecuencia de muestreo: {f_sample:1.5} hz")
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

        return fig