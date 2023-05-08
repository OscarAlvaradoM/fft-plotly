from dash import dcc, html
import dash_bootstrap_components as dbc

from styles import COLORS_STYLE, SIDEBAR_STYLE, UPLOAD_STYLE, BUTTON_STYLE

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
        html.H2("Mediciones", className="display-4", style={"color":COLORS_STYLE["text_color"]}),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        html.P("Selecciona el archivo que quieras visualizar:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        upload_object,
        html.Br(),
        # dbc.Nav(
        #     [
        #         dbc.NavLink("FFT", href="/", active="exact", style={"text-align":"center"}),
        #         dbc.NavLink("Espectrograma", href="/page_1", active="exact", style={"text-align":"center"})
        #     ],
        #     vertical=False,
        #     pills=True,
        #     justified=True
        # ),
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

button = html.Div(
    [
        dbc.Button("Agregar Señal", outline=True, color="info", id="button-add-signal", n_clicks=None),
    ],
    className="d-grid gap-2",
)

modal = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Configure la onda a simular:"), close_button=True),
                dbc.ModalBody([
                        dcc.Dropdown(['Sinusoidal', 'Cuadrada', 'Triangular', 'Sierra'], id="tipo-onda", placeholder="Selecciona un tipo de onda", value=None),
                        dbc.Label("Número de periodos:"),
                        dbc.Input(id="numero-periodos", type="number", placeholder="Ingresa número de periodos", min=1, value=None),
                        dbc.Label("Amplitud [V]:"),
                        dbc.Input(id="amplitud", type="number", placeholder="Ingresa la amplitud de la señal", min=1, value=None),
                        dbc.Label("Resolución:"),
                        dbc.Input(id="resolucion", type="number", placeholder="Ingresa la resolución", min=1, value=None),
                    ]),
                dbc.ModalFooter(
                    [
                        dbc.Button("OK", color="primary", id="ok-button", n_clicks=None),
                        dbc.Button("Cancelar", id="cancel-button", n_clicks=None),
                    ]
                ),
            ],
            id="modal-centered",
            centered=True,
            is_open=False,
)

sidebar2 = html.Div(
    [
        html.H2("Simulación", className="display-4", style={"color":COLORS_STYLE["text_color"]}),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        button,
        modal,
        # html.P("Selecciona la función que quieras simular:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        # dcc.Dropdown(['Sinusoidal', 'Cuadrada', 'Triangular', 'Sierra'], id="tipo-ondas", placeholder="Selecciona un tipo de onda"),
        # html.Br(),
        # dbc.Nav(
        #     [
        #         dbc.NavLink("FFT", href="/", active="exact", style={"text-align":"center"}),
        #         dbc.NavLink("Espectrograma", href="/page_1", active="exact", style={"text-align":"center"})
        #     ],
        #     vertical=False,
        #     pills=True,
        #     justified=True
        # ),
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