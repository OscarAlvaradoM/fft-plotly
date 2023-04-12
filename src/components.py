from dash import dcc, html
import dash_bootstrap_components as dbc

from styles import COLORS_STYLE, SIDEBAR_STYLE, UPLOAD_STYLE

# -------------------------------- Objetos base------------------------------------------------------------------------------------
upload_object = dcc.Upload(
        id='upload-data',
        children=html.Div(['Arrastra y suelta o ', html.A('Selecciona archivos')]),
        style=UPLOAD_STYLE,
        # Vemos si podemos escoger múltiples archivos a la vez. Por el momento no queremos esto.
        multiple=False
    )

sidebar = html.Div(
    [
        html.H2("Señales", className="display-4", style={"color":COLORS_STYLE["text_color"]}),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        html.P("Selecciona el archivo que quieras visualizar:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        upload_object,
        html.Br(),
        dbc.Nav(
            [
                dbc.NavLink("FFT", href="/", active="exact", style={"text-align":"center"}),
                dbc.NavLink("Espectrograma", href="/page_1", active="exact", style={"text-align":"center"})
            ],
            vertical=False,
            pills=True,
            justified=True
        ),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        html.Div([
        html.P("Número de muestras:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='numero-muestras', style={"color":COLORS_STYLE["plot_color_1"]}),
        html.P("Frecuencia de muestreo:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='frecuencia-muestreo', style={"color":COLORS_STYLE["plot_color_1"]}),
        html.P("Resolución en frecuencia:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='resolucion-frecuencia', style={"color":COLORS_STYLE["plot_color_2"]})
        ], style={"display":"None"}, id="propiedades1")
    ],
    style=SIDEBAR_STYLE,
)

sidebar2 = html.Div(
    [
        html.H2("Señales", className="display-4", style={"color":COLORS_STYLE["text_color"]}),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        html.P("Selecciona la función que quieras simular:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        dcc.Dropdown(['Sinusoidal', 'Cuadrada', 'Triangular', 'Sierra']),
        html.Br(),
        dbc.Nav(
            [
                dbc.NavLink("FFT", href="/", active="exact", style={"text-align":"center"}),
                dbc.NavLink("Espectrograma", href="/page_1", active="exact", style={"text-align":"center"})
            ],
            vertical=False,
            pills=True,
            justified=True
        ),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        html.Div([
        html.P("Número de muestras:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='numero-muestras-sim', style={"color":COLORS_STYLE["plot_color_1"]}),
        html.P("Frecuencia de muestreo:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='frecuencia-muestreo-sim', style={"color":COLORS_STYLE["plot_color_1"]}),
        html.P("Resolución en frecuencia:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='resolucion-frecuencia-sim', style={"color":COLORS_STYLE["plot_color_2"]})
        ], style={"display":"None"}, id="propiedades2")
    ],
    style=SIDEBAR_STYLE,
)