from dash import dcc, html
import dash_bootstrap_components as dbc

from styles import COLORS_STYLE, SIDEBAR_STYLE, UPLOAD_STYLE, CENTERED_CONTENT_STYLE

# -------------------------------- Objetos base------------------------------------------------------------------------------------
upload_object = dcc.Upload(
        id='upload-data',
        children=html.Div(['Arrastra y suelta o ', html.A('Selecciona archivos')]),
        style=UPLOAD_STYLE,
        # Vemos si podemos escoger múltiples archivos a la vez. Por el momento no queremos esto.
        multiple=False
    )

spectrogram_button = html.Div(
    [
        dbc.Button("Espectrograma", color="info", id="button-spectrogram", n_clicks=None),
    ],
    className="d-grid gap-2",
)

modal_spectrogram = dbc.Modal(
            [
                #dbc.ModalHeader(dbc.ModalTitle("Espectrograma de la señal medida:"), close_button=True),
                dcc.Graph(figure=None, id='grafica-modal-spectrogram'),
            ],
            id="modal-spectrogram",
            centered=True,
            is_open=False,
)

sidebar = html.Div(
    [
        html.H2("Mediciones", className="display-4", style={"color":COLORS_STYLE["text_color"]}),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        html.P("Selecciona el archivo que quieras visualizar:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        upload_object,
        html.Br(),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        html.Div([
        html.P("Número de muestras:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='numero-muestras', style={"color":COLORS_STYLE["plot_color_1"]}),
        html.P("Frecuencia de muestreo:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='frecuencia-muestreo', style={"color":COLORS_STYLE["plot_color_1"]}),
        html.P("Resolución en frecuencia:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        html.P(id='resolucion-frecuencia', style={"color":COLORS_STYLE["plot_color_2"]}),
        spectrogram_button,
        modal_spectrogram
        ], style={"display":"None"}, id="propiedades1")
    ],
    style=SIDEBAR_STYLE,
)

add_button = html.Div(
    [
        dbc.Button("Sumar señales", outline=True, color="info", id="button-add-signal", n_clicks=None),
    ],
    className="d-grid gap-2",
)

reset_button = html.Div(
    [
        dbc.Button("Reiniciar", color="info", id="button-reset-signal", n_clicks=None, style={"display":"None"}),
    ],
    className="d-grid gap-2 d-md-flex justify-content-md-end",
)

other_signals_button = html.Div(
    [
        dbc.Button("Simular señal", outline=True, color="info", id="button-other-signals", n_clicks=None),
    ],
    className="d-grid gap-2",
)

reset_button2 = html.Div(
    [
        dbc.Button("Reiniciar", color="info", id="button-reset-other-signals", n_clicks=None, style={"display":"None"}),
    ],
    className="d-grid gap-2 d-md-flex justify-content-md-end",
)

modal = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Configuración de la señal:"), close_button=True),
                dbc.ModalBody([
                        # dbc.Label("Tipo de Onda:"),
                        # dcc.Dropdown(['Sinusoidal', 'Cuadrada', 'Triangular', 'Sierra'], id="tipo-onda", placeholder="Selecciona un tipo de onda", value=None),
                        dbc.Label("Frecuencia [Hz]:"),
                        dbc.Input(id="frecuencia", type="number", placeholder="Ingresa la frecuencia", min=1, value=None),
                        dbc.Label("Amplitud pico  a pico [V]:"),
                        dbc.Input(id="amplitud", type="number", placeholder="Ingresa la amplitud de la señal", min=1, value=None),
                        # dbc.Label("Resolución:"),
                        # dbc.Input(id="resolucion", type="number", placeholder="Ingresa la resolución", min=1, value=None),
                    ]),
                dbc.ModalFooter(
                    [
                        dbc.Button("OK", color="primary", id="ok-button", n_clicks=None),
                        dbc.Button("Cancelar", id="cancel-button", n_clicks=None),
                    ]
                ),
            ],
            id="modal-signal-adding",
            centered=True,
            is_open=False,
)

modal_other_signals = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Configuración de la señal:"), close_button=True),
                dbc.ModalBody([
                        dbc.Label("Tipo de Onda:"),
                        dcc.Dropdown(['Cuadrada', 'Triangular', 'Sierra'], id="tipo-onda", placeholder="Selecciona un tipo de onda", value=None),
                        dbc.Label("Frecuencia [Hz]:"),
                        dbc.Input(id="frecuencia-other-signals", type="number", placeholder="Ingresa la frecuencia", min=1, value=None),
                        dbc.Label("Amplitud pico  a pico [V]:"),
                        dbc.Input(id="amplitud-other-signals", type="number", placeholder="Ingresa la amplitud de la señal", min=1, value=None),
                        # dbc.Label("Resolución:"),
                        # dbc.Input(id="resolucion", type="number", placeholder="Ingresa la resolución", min=1, value=None),
                    ]),
                dbc.ModalFooter(
                    [
                        dbc.Button("OK", color="primary", id="ok-button-other-signals", n_clicks=None),
                        dbc.Button("Cancelar", id="cancel-button-other-signals", n_clicks=None),
                    ]
                ),
            ],
            id="modal-other-signals",
            centered=True,
            is_open=False,
)

sidebar2 = html.Div(
    [
        html.H2("Suma", className="display-4", style={"color":COLORS_STYLE["text_color"]}),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        add_button,
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        modal,
        # html.Div([
        # html.P("Número de muestras:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        # html.P(id='numero-muestras-sim', style={"color":COLORS_STYLE["plot_color_1"]}),
        # html.P("Frecuencia de muestreo:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        # html.P(id='frecuencia-muestreo-sim', style={"color":COLORS_STYLE["plot_color_1"]}),
        # html.P("Resolución en frecuencia:", className="lead", style={"color":COLORS_STYLE["text_color"]}),
        # html.P(id='resolucion-frecuencia-sim', style={"color":COLORS_STYLE["plot_color_2"]})
        # ], style={"display":"None"}, id="propiedades2"),
        reset_button,
    ],
    style=SIDEBAR_STYLE,
)

sidebar3 = html.Div(
    [
        html.H2("Simulación", className="display-4", style={"color":COLORS_STYLE["text_color"]}),
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        other_signals_button,
        html.Hr(style={"color":COLORS_STYLE["text_color"]}),
        modal_other_signals,
        reset_button2
    ],
    style=SIDEBAR_STYLE,
)

initial_content_add_signals = [
        html.H5("Presione 'Sumar señales' en el panel de la izquierda para sumar señales sinusoidales.", style={"color":COLORS_STYLE["text_color"]}),
        html.H1("Simulación de datos.", style=CENTERED_CONTENT_STYLE),
    ]

initial_content_other_signals = [
        html.H5("Presione 'Simular señal' en el panel de la izquierda para visualizar otro tipo de señales.", style={"color":COLORS_STYLE["text_color"]}),
        html.H1("Simulación de datos.", style=CENTERED_CONTENT_STYLE),
    ]


initial_content_measure = [
        html.H5("Arrastre o presione en el área punteada del panel de la izquierda para observar datos medidos.", style={"color":COLORS_STYLE["text_color"]}),
        html.H1("Medición de datos.", style=CENTERED_CONTENT_STYLE)
    ]

initial_error_content_measure = [
        html.H5(f'Hubo un error procesando este archivo, por favor asegúrate que es un archivo de tipo .csv o .xls', style={"color":COLORS_STYLE["text_color"]}),
    ]
