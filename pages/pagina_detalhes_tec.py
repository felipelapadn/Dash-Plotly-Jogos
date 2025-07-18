from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def limite_superior(data):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1

    return q3 + 1.5 * iqr

IMG_STYLE = {
    "border-radius": "8px",
    'height': '200px'
}

df = pd.read_csv("./data/processed/games_march2025_cleaned.csv")
df = df.sort_values(by="recommendations", ascending=False)

colors = ['lightblue' for i in range(10)]

series_genero = df.tags_sep.apply(lambda x: eval(x))
stack_genero = list()
for i in series_genero:
    stack_genero.extend(i)
stack_genero = set(stack_genero)

fig = go.Figure()
fig_age = go.Figure()

layout = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.DatePickerRange(
            id='filtro-data',
            min_date_allowed=df['release_date'].min(),
            max_date_allowed=df['release_date'].max(),
            start_date=df['release_date'].min(),
            end_date=df['release_date'].max(),
            display_format='DD-MM-YYYY'
        )),
        dbc.Col(dcc.Dropdown(
            id='filtro-genero',
            options=[
                {'label': genero, 'value': genero} for genero in sorted(stack_genero)
            ],
            placeholder='Selecione o gênero',
            searchable=True, 
            clearable=True, 
            multi=False,
            style={'width': '100%'}
        ))
    ]), 
    dbc.Row([
        dcc.Graph(id='grafico-sistemas', figure=fig)
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='grafico-age', figure=fig_age), style={"height": "100%"}
        ),
    ]),
])

@callback(
    Output('grafico-sistemas', 'figure'),
    Input('filtro-data', 'start_date'),
    Input('filtro-data', 'end_date'),
    Input('filtro-genero', 'value'),

)
def atualizar_grafico(start_date, end_date, value):
    filtered_df = df.copy()

    if value:
        filtered_df = filtered_df[filtered_df['tags_sep'].apply(lambda tags: value in tags)]

    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['release_date'] >= start_date) &
            (filtered_df['release_date'] <= end_date)
        ]

    filtered_df.reset_index(drop=True, inplace=True)

    df_mean_price_publisher = filtered_df[["publisher", "price"]].groupby("publisher").mean().sort_values("price", ascending=False)[:5].reset_index()
    abreviacoes = {
        'Windows': 'Win',
        'Windows+Mac': 'Win+Mac',
        'Windows+Mac+Linux': 'All',
        'Windows+Linux': 'Win+Linux',
        'Mac': 'Mac',
    }
    
    filtered_df['plataformas'] = filtered_df.apply(
        lambda row: '+'.join([
            plat for plat, available in zip(['Windows', 'Mac', 'Linux'], [row['windows'], row['mac'], row['linux']])
            if available
        ]), axis=1
    )

    combo_counts = filtered_df['plataformas'].value_counts().reset_index()
    combo_counts.columns = ['Plataformas', 'Quantidade']

    df_mean_price_publisher['publisher_abrev'] = df_mean_price_publisher['publisher'].str.slice(0, 12) + "…"
    combo_counts['Plataformas_Abrev'] = combo_counts['Plataformas'].map(abreviacoes)

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            "Distribuição de Jogos por Combinação de Plataformas",
            "Preço médio por Estúdio"
        ),
        shared_yaxes=False
    )

    # Gráfico 1: Distribuição por plataforma (abreviado)
    fig.add_trace(
        go.Bar(
            x=combo_counts['Plataformas_Abrev'],
            y=combo_counts['Quantidade'],
            text=combo_counts['Quantidade'],
            textposition='outside',
            marker_color='lightblue',
            name="Plataformas"
        ),
        row=1, col=1
    )

    # Gráfico 2: Preço médio por publisher (abreviado)
    fig.add_trace(
        go.Bar(
            x=df_mean_price_publisher['publisher_abrev'],
            y=df_mean_price_publisher['price'],
            text=df_mean_price_publisher['price'].map(lambda p: f"${p:.2f}"),
            textposition='outside',
            marker_color='lightblue',
            name="Preço"
        ),
        row=1, col=2
    )

    fig.update_layout(
        template='plotly_white',
        height=600,
        showlegend=False
    )

    fig.update_xaxes(title_text='Plataformas', tickangle=-45, row=1, col=1)
    fig.update_yaxes(title_text='Número de Jogos', domain=[0.0, 0.95], row=1, col=1)

    fig.update_xaxes(title_text='Estúdio', tickangle=-45, row=1, col=2)
    fig.update_yaxes(title_text='Preço ($)', domain=[0.0, 0.95], row=1, col=2)

    return fig

@callback(
    Output('grafico-age', 'figure'),
    Input('filtro-data', 'start_date'),
    Input('filtro-data', 'end_date'),
    Input('filtro-genero', 'value'),
)
def mostrar_imagem(start_date, end_date, value):
    filtered_df = df.copy()

    if value:
        filtered_df = filtered_df[filtered_df['tags_sep'].apply(lambda tags: value in tags)]

    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['release_date'] >= start_date) &
            (filtered_df['release_date'] <= end_date)
        ]

    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df["len_supported_languages"] = filtered_df["supported_languages"].apply(lambda x: len(eval(x)))
    
    limite_superior_positive = limite_superior(filtered_df.positive)
    limite_superior_peak = limite_superior(filtered_df.peak_ccu)
        
    df_filtered_age = filtered_df.query("required_age == 0 and positive < @limite_superior_positive and peak_ccu < @limite_superior_peak")
    fig_age = go.Figure()

    fig_age.add_trace(go.Scatter(
        x=df_filtered_age["positive"],
        y=df_filtered_age["price"],
        mode='markers',
        marker=dict(
            # size=df_filtered_age["required_age"],
            color=df_filtered_age["peak_ccu"],
            colorscale='blues',
            showscale=True,
            colorbar=dict(title="Idade Requerida")
        ),
        text=df_filtered_age["name"],
        hovertemplate=(
            "<b>%{text}</b><br>" +
            "Preço: R$ %{y:.2f}<br>" +
            "Qtd. Avaliações Positivas: %{x:.1f}<br>" +
            "Jogadores Ativos Simultaneamente: %{marker.color}"
        )
    ))
    fig_age.update_traces(marker_size=20)

    fig_age.update_layout(
        title="Como o Preço de Jogos e o Pico de Jogadores Ativos Simultaneamente Influenciam nas Avaliações Positivas",
        xaxis_title="Percentual de Avaliações Positivas (%)",
        yaxis_title="Preço ($)",
        template="plotly_white",
        height=600,
        annotations=[
            dict(
                text="Este gráfico foi elaborado com base em jogos de classificação livre para jogar e dados abaixo do 3º quartil, a fim de evitar outliers.",
                xref="paper",
                yref="paper",
                x=0.49,
                y=1.02,  
                showarrow=False,
                font=dict(size=14, color="grey"),
                xanchor='center',
                yanchor='bottom'
            )
        ]
    )
    
    return fig_age

        
    