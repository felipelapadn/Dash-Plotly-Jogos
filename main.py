import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from pages.pagina_indv_jogo import layout as pagina_indv_jogo
from pages.pagina_detalhes_tec import layout as pagina_detalhes



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard de Jogos"

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Dashboard de Jogos", className="display-5"),
        html.Hr(),
        html.P("Dashboard interativo com visualizações sobre jogos mais recomendados e estatísticas da base Steam.", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Top 10 Jogos Mais Recomendados", href="/", active="exact"),
                dbc.NavLink("Visão Geral da Base de Dados", href="/pagina_detalhes", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return pagina_indv_jogo  
    elif pathname == "/pagina_detalhes":
        return pagina_detalhes
 
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run(debug=True)