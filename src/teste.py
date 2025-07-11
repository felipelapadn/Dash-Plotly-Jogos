import base64
import dash
from dash import dcc, html, Output, Input
import plotly.express as px
import pandas as pd

# Dados de exemplo
df = pd.read_csv("./data/processed/games_march2025_cleaned.csv")

# Gráfico de barras
fig = px.bar(df[:10], x='name', y='price', title='Jogos Mais Vendidos')

# App Dash
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='grafico-vendas', figure=fig),
    html.Div(id='imagem-produto')
])

# Callback: Atualiza imagem ao clicar
@app.callback(
    Output('imagem-produto', 'children'),
    Input('grafico-vendas', 'clickData')
)
def mostrar_imagem(clickData):
    if clickData:
        produto = clickData['points'][0]['x']
        url_imagem = df[df['name'] == produto]['header_image'].values[0]

        return html.Img(src=url_imagem, style={'height': '200px'})
    return "Clique em um item para ver a imagem."

if __name__ == '__main__':
    app.run(debug=True)
