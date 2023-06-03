# El estilo para los colores que utilizamos en general.
COLORS_STYLE = {"text_color": "#D8D8D8",
                "plot_color_1": "#F4D44D",
                "plot_color_2": "#F45060",
                "background_color_1": "#1E1E1E",
                "background_color_2": "#323130"}

# El estilo para el panel de la izquierda.
SIDEBAR_STYLE = {
    "padding": "2rem 1rem",
    "position": "fixed",
    "top": "42px",
    "height":"100%",

    "left": 0,
    "bottom": 0,

    "min-height":"1000px",
    "width":"20rem",

    "background-color": COLORS_STYLE["background_color_1"]
}

# El estilo para el contenido principal, es decir, donde se encontrarán las gráficas.
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    "background-color": COLORS_STYLE["background_color_2"],
    "position": "fixed"
}

INITIAL_CONTENT_MEASURE_STYLE = {
    # "margin-left": "10rem",
    # "margin-right": "0rem",
    # "padding": "1.5rem 1rem",
    # "background-color": COLORS_STYLE["background_color_2"]
    "margin-left": "20rem",
    "margin-top": "42px",
    "padding": "1.5rem 2rem",
    "background-color": COLORS_STYLE["background_color_2"]
}

INITIAL_CONTENT_ADD_STYLE = {
    "margin-left": "20rem",
    "margin-top": "42px",
    "padding": "1.5rem 2rem",
    "background-color": COLORS_STYLE["background_color_2"]
}

INITIAL_CONTENT_OTHER_STYLE = {
    "margin-left": "20rem",
    "margin-top": "42px",
    "padding": "1.5rem 2rem",
    "background-color": COLORS_STYLE["background_color_2"]
}

CENTERED_CONTENT_STYLE = {
    "color":COLORS_STYLE["text_color"],
    "min-height":"600px",
    'height': '100%',
    'textAlign': 'center',
    "padding": "300px 0",
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

# Este es el estilo de las pestañas que no están seleccionadas.
TAB_STYLE = {
    'border': 'none',
    'boxShadow': 'inset 0px -1px 0px 0px lightgrey',
    'background': 'white',
    'paddingTop': "5px",
    'paddingBottom': 0,
    'height': '42px',
    'background': '#1E1E1E',
    'color' : '#D8D8D8',
}

TAB_STYLE_2 = {
    'top': '420px',
    'border': 'none',
    'boxShadow': 'inset 0px -1px 0px 0px lightgrey',
    'background': 'white',
    'paddingTop': "5px",
    'paddingBottom': 0,
    'height': '42px',
    'background': '#1E1E1E',
    'color' : '#D8D8D8',
}

# Este es el estilo de las pestañas en general.
TABS_STYLE = {
    "position": "fixed",
    "width":"100%",
    "min-width":"1000px",
    "height":"auto"
}

TABS_STYLE_2 = {
    "position": "relative",
    "top": "42px",
    "margin-left": "20rem",
    "width":"relative",
    "min-width":"1000px",
    "height":"auto"
}

# Este es el estilo de las pestañas que están seleccionadas.
SELECTED_STYLE = {
    'boxShadow': 'none',
    'borderLeft': 'none',
    'borderRight': 'none',
    'borderTop': 'none',
    'borderBottom': '2px #004A96 solid',
    'background': '#000000',
    'paddingTop': "5px",
    'paddingBottom': 0,
    'height': '42px',
    'color' : '#D8D8D8',
}

SELECTED_STYLE_2 = {
    'top': '420px',
    'boxShadow': 'none',
    'borderLeft': 'none',
    'borderRight': 'none',
    'borderTop': 'none',
    'borderBottom': '2px #004A96 solid',
    'background': '#000000',
    'paddingTop': "5px",
    'paddingBottom': 0,
    'height': '42px',
    'color' : '#D8D8D8',
}

BUTTON_STYLE = {
    'width': '100%',
    'height': '60px',
    'width': '240px', 
    'height': '40px', 
    'cursor': 'pointer', 
    'border': '0px', 
    'border-radius': '5px', 
    'borderBottom': '2px #004A96 solid',
    'borderTop': '2px #004A96 solid',
    'borderLeft': '2px #004A96 solid',
    'borderRight': '2px #004A96 solid',
    'background-color': '#000000', 
    'color': 'white', 
    'text-transform': 'uppercase', 
    'font-size': '15px',
    'hover': {'background-color': '#555555'}
}

SIGNALS_STYLE = {
    "margin-left": "20rem",
    "margin-top": "42px",
    "padding": "1.5rem 2rem",
    "background-color": COLORS_STYLE["background_color_2"]
}