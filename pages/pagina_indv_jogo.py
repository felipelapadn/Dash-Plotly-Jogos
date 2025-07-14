import base64
import dash
from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

IMG_STYLE = {
    "border-radius": "8px",
    'height': '200px'
}

df = pd.read_csv("./data/processed/games_march2025_cleaned.csv")
df = df.sort_values(by="recommendations", ascending=False)

colors = ['lightblue' for i in range(10)]

fig = px.bar(df[:10], x='recommendations', y='name', title='Jogos Mais Recomendados', orientation='h',
                 category_orders={'name': df['name'].tolist()})
fig.update_traces(marker_color=colors) 
fig.update_layout(
        template='plotly_white',
)

fig_atividade = go.Figure()

fig_jogo_preco = go.Figure()

layout = dbc.Container([
    html.Br(),
    dbc.Row([
        dcc.DatePickerRange(
            id='filtro-data',
            min_date_allowed=df['release_date'].min(),
            max_date_allowed=df['release_date'].max(),
            start_date=df['release_date'].min(),
            end_date=df['release_date'].max(),
            display_format='DD-MM-YYYY'
        )
    ]), 
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='grafico-jogos', figure=fig), style={"height": "100%"}, width=7
        ),
        dbc.Col(
            dbc.Card([html.Div(id='imagem-produto')], style={"maxWidth": "100%"}),
            width=4,
            style={"display": "flex", "alignItems": "center"}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='grafico-media-preco', figure=fig_jogo_preco), style={"height": "100%"}, width=7
        ),
        dbc.Col(
            dcc.Graph(id='grafico-atividade', figure=fig_atividade), style={"height": "100%"}, width=4
        ),
    ]),
])

@callback(
    Output('grafico-jogos', 'figure', allow_duplicate=True),
    Input('filtro-data', 'start_date'),
    Input('filtro-data', 'end_date'),
    prevent_initial_call=True
)
def atualizar_grafico(start_date, end_date):
    if start_date is None or end_date is None:
        filtered_df = df.copy()
    else:
        filtered_df = df[(df['release_date'] >= start_date) & (df['release_date'] <= end_date)]
        filtered_df.reset_index(drop=True, inplace=True)

    fig = px.bar(filtered_df[:10], x='recommendations', y='name', title='Jogos Mais Recomendados', orientation='h',
                 category_orders={'name': filtered_df[:10]['name'].tolist()}, color="lightblue")
    
    fig.update_layout(
        template='plotly_white',
    )
    
    return fig

@callback(
    Output('imagem-produto', 'children'),
    Input('grafico-jogos', 'clickData'),
    Input('filtro-data', 'start_date'),
    Input('filtro-data', 'end_date'),
)
def mostrar_imagem(clickData, start_date, end_date):
    if start_date is None or end_date is None:
        filtered_df = df.copy()
    else:
        filtered_df = df[(df['release_date'] >= start_date) & (df['release_date'] <= end_date)]
        filtered_df.reset_index(drop=True, inplace=True)
        
    if clickData:
        jogo = clickData['points'][0]['y']
        url_imagem = filtered_df[filtered_df['name'] == jogo]['header_image'].values[0]

        return html.Img(src=url_imagem, style=IMG_STYLE)
    else:
        url_imagem = filtered_df['header_image'].values[0]
        return html.Img(src=url_imagem, style=IMG_STYLE)
    

@callback(
    Output('grafico-atividade', 'figure'),
    Input('grafico-jogos', 'clickData'),
    Input('filtro-data', 'start_date'),
    Input('filtro-data', 'end_date'),
)
def atualizar_grafico_atividade(clickData, start_date, end_date):
    if start_date is None or end_date is None:
        filtered_df = df.copy()
    else:
        filtered_df = df[(df['release_date'] >= start_date) & (df['release_date'] <= end_date)]
        filtered_df.reset_index(drop=True, inplace=True)
        
    top10 = filtered_df[:10]
    x = top10.recommendations.values
    y = top10.peak_ccu.values
    names = top10.name.values

    if clickData:
        jogo = clickData['points'][0]['y']
        idx = filtered_df[filtered_df['name'] == jogo]['header_image'].index.values[0]
    else:
        idx = 0

    fig_atividade = go.Figure()

    fig_atividade.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(size=10, color='lightblue'),
        text=names
    ))

    fig_atividade.add_trace(go.Scatter(
        x=[x[idx]],
        y=[y[idx]],
        mode='markers+text',
        marker=dict(size=14, color='crimson', symbol='circle'),
        textposition='top center',
        text=names[idx]
    ))

    fig_atividade.update_layout(
        title='Relação atividade x recomendações',
        xaxis_title='Recommendations',
        yaxis_title='Peak_ccu',
        template='plotly_white',
        showlegend=False,
        height=470,  
        width=500,
        margin=dict(t=75)  
    )
    
    return fig_atividade

@callback(
    Output('grafico-media-preco', 'figure'),
    Input('grafico-jogos', 'clickData'),
    Input('filtro-data', 'start_date'),
    Input('filtro-data', 'end_date'),
)
def atualizar_grafico_atividade(clickData, start_date, end_date):
    
    if start_date is None or end_date is None:
        filtered_df = df.copy()
    else:
        filtered_df = df[(df['release_date'] >= start_date) & (df['release_date'] <= end_date)]
        filtered_df.reset_index(drop=True, inplace=True)
        
    if clickData:
        jogo = clickData['points'][0]['y']
        idx = filtered_df[filtered_df['name'] == jogo]['header_image'].index.values[0]
    else:
        idx = 0
        jogo = filtered_df.name.iloc[0]
    prices = filtered_df[:10].price.values
    colors = ['crimson' if i == idx else 'lightblue' for i in range(len(prices))]
    media_sem_idx0 = np.mean(np.delete(prices, idx))

    fig_jogo_preco = go.Figure()

    fig_jogo_preco.add_trace(go.Bar(
        x=[i.split(":")[0] for i in filtered_df[:10].name.values],
        y=prices,
        marker_color=colors,
        text=[f"{p:.2f}" for p in prices],
        textposition="outside",
        name="Jogo Destacado"
    ))

    fig_jogo_preco.add_trace(go.Scatter(
        x=[i.split(":")[0] for i in filtered_df[:10].name.values],
        y=[media_sem_idx0]*len(prices),
        mode='lines',
        line=dict(color='green', dash='dash'),
        name=f'Média (sem {jogo})'
    ))

    fig_jogo_preco.update_layout(
        title=f'Gráfico de Preços com Destaque no jogo {jogo}',
        xaxis_title='Jogo',
        yaxis_title='Preço ($)',
        showlegend=True,
        bargap=0.2,
        template='plotly_white',
        legend=dict(
            orientation="h",       
            yanchor="bottom",       
            y=1.02,                 
            xanchor="center",     
            x=0.5                   
        ),
        margin=dict(t=75)
    )
    
    return fig_jogo_preco
