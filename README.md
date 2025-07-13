# Dashboard para Monitoramento de Jogos Digitais

### Objetivo Geral

1. Oferecer uma visão centralizada e intuitiva dos principais indicadores de desempenho dos jogos (como pico de jogadores simultâneos, tempo de jogo, preço e avaliações).
2. Avaliar tanto o engajamento (playtime, playtime mediano) quanto a satisfação dos usuários (`pct_pos_total`, `recommendations`) em tempo real.
3. Mensurar o impacto de estratégias comerciais (preço e descontos) sobre o comportamento do jogador e receita estimada.
4. Identificar oportunidades de loteamento e crescimento por plataforma, idioma, DLCs e temas mais populares (tags).
5. Apoiar decisões táticas e estratégicas das equipes de produto, marketing e infraestrutura através de comparações, benchmarks e insights acionáveis.

### Público‑alvo

O dashboard é voltado para:

* **Gerentes de Produto e Marketing**: para entender o que impacta o engajamento e monetização, identificando títulos com potencial para promoção ou investimento adicional;
* **Analistas de Dados e Business Intelligence**: para encontrar padrões, outliers e tendências na utilização, reviews e vendas;
* **Equipes de Infraestrutura e Operações**: para monitorar pico de uso (`peak_ccu`), planejar capacidade de servidores e evitar falhas nos lançamentos;
* **Executivos e Stakeholders**: que precisam de uma visão consolidada e visual do desempenho do portfólio, para embasar decisões estratégicas com dados confiáveis.

Com base nas ideias acima, as colunas que serão priorizadas serão:

1. **appid** (int64):
   ID único atribuído pelo Steam a cada jogo. Útil para cruzamentos com APIs ou bases externas.

2. **name** (object):
   Nome do jogo/título da aplicação.

3. **release\_date** (datetime64\[ns]):
   Data oficial de lançamento do jogo na plataforma Steam.

4. **required\_age** (int64):
   Idade mínima recomendada/necessária para jogar, conforme classificação etária da Steam.

5. **price** (float64):
   Preço atual do jogo, geralmente em dólares. Valores típicos variam de 0 (grátis) até cerca de 59,99.

6. **dlc\_count** (int64):
   Quantidade de DLCs (conteúdo adicional pago) associados ao jogo.

7. **header\_image** (object):
   URL da imagem de cabeçalho/banner do jogo, usada na interface do Steam.

8. **windows** (bool):
   Indica se o jogo tem suporte ao sistema operacional Windows (True/False).

9. **mac** (bool):
   Indica se o jogo tem suporte ao macOS.

10. **linux** (bool):
    Indica se o jogo tem suporte ao Linux.

11. **metacritic\_score** (int64):
    Nota agregada do Metacritic (0–100), refletindo avaliações da mídia especializada.

12. **recommendations** (int64):
    Total de recomendações positivas de usuários no Steam — geralmente representando quantos "curtiram" o jogo.

13. **supported\_languages** (object):
    Lista de idiomas suportados na interface do jogo (legendas e UI).

14. **full\_audio\_languages** (object):
    Idiomas disponíveis com áudio completo no jogo (voltações).

15. **publishers** (object):
    Empresa(s) publicadoras responsáveis pela distribuição do jogo.

16. **positive** (int64):
    Número bruto de análises positivas (reviews) dos usuários.

17. **negative** (int64):
    Número bruto de análises negativas dos usuários.

18. **average\_playtime\_forever** (int64):
    Tempo médio de jogo (em minutos) por todos os usuários que jogaram.

19. **median\_playtime\_forever** (int64):
    Tempo mediano de jogo (minutos) por todos os usuários — menos sensível a valores extremos.

20. **discount** (int64):
    Percentual de desconto atual aplicado (0 se não estiver em promoção, por exemplo, 50 para metade do preço).

21. **peak\_ccu** (int64):
    *Pico de usuários simultâneos* — maior número de jogadores online ao mesmo tempo durante a existência do jogo.

22. **tags** (object):
    Conjunto de etiquetas/temas atribuídos pelos usuários (ex.: `"Action;Multiplayer;Open World"`).

23. **pct\_pos\_total** (int64):
    Percentual de avaliações positivas em relação ao total de análises:

    ```
    pct_pos_total = (positive / (positive + negative)) * 100  
    ```

    Representa a proporção de reviews positivas — um indicador direto da satisfação geral dos jogadores.

24. **num\_reviews\_total** (int64):
    Soma total de avaliações: `positive + negative`.


### Resumo dos dados

| Coluna                                                          | Utilidade                                                            |
| --------------------------------------------------------------- | -------------------------------------------------------------------- |
| **price**, **discount**                                         | Avaliar impacto de promoções sobre vendas                            |
| **dlc\_count**, **tags**                                        | Analisar diversidade de conteúdo e segmentos de interesse            |
| **peak\_ccu**                                                   | Medir popularidade em tempo real & dimensionamento de infraestrutura |
| **pct\_pos\_total**, **recommendations**, **metacritic\_score** | Avaliar qualidade percebida e reputação geral                        |
| **average/median playtime**                                     | Entender engajamento e retenção do jogador                           |

### Link do Dataset

Baixe o dataset em: [Steam Games Dataset 2025](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset)         
Em seguida, coloque o arquivo baixado em `data/raw/` caso queira rodar o notebook de tratamento.