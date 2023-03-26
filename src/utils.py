import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Onda():
    def __init__(self, file):
        raw_file = pd.read_csv(file)
        self.metadata = raw_file.iloc[:13,:]
        self.data = raw_file.iloc[14:,:]
            
    def plot_fourier(self, f_sample=0.001):

        data = self.data
        fig = make_subplots(rows=1, cols=2)    

        fig.add_trace(go.Scatter(x=data.iloc[:,0], y=data.iloc[:,1], name = "Medición"),row=1, col=1)

        ffty = np.fft.fft(data.iloc[:,1])

        N = len(data)
        f_interval = f_sample / N
        hertz = np.arange(N)*f_interval
        hertz = hertz - np.ceil(max(hertz)/2)
        specs = np.fft.fftshift(20*np.log10(ffty))
        specs = [np.linalg.norm(spec) for spec in specs]
        fig.add_trace(go.Scatter(x=hertz, y=specs, name = "Fourier"),row=1, col=2)

        fig.update_layout(height=600, width=950, 
                          #title_text=f"Resolución: {resolution} s<br>Frecuencia de muestreo: {f_sample:1.5} hz")
                          title_text=f"Frecuencia de muestreo: {f_sample:1.5} hz")

        fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1),
        margin=dict(l=0, r=0, t=100, b=100),)

        return fig