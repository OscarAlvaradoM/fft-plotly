COLORS_STYLE = {"text_color": "#D8D8D8",
                "plot_color_1": "#F4D44D",
                "plot_color_2": "#F45060",
                "background_color_1": "#1E1E1E",
                "background_color_2": "#323130"}

# El estulo para el panel de la izquierda.
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": COLORS_STYLE["background_color_1"]
}

# El estilo para el contenido principal, es decir, donde se encontrarán las gráficas.
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    "background-color": COLORS_STYLE["background_color_2"]
}

INITIAL_CONTENT_STYLE = {
    "margin-left": "10rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    "background-color": COLORS_STYLE["background_color_2"]
}

# El estilo para el botón de carga de archivos.
UPLOAD_STYLE = {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '5px',
            'color': COLORS_STYLE["text_color"]
        }