# NASA Space Apps 2025

## Projeto **AeroVigil**
> O hub definitivo de pesquisa e inteligência sobre tempo e qualidade do ar.

---

## Resumo

O **AeroVigil** é um hub tecnológico de inteligência ambiental, desenvolvido para **monitorar, prever e alertar sobre a qualidade do ar em tempo real**.  
A plataforma integra dados de satélite (**NASA TEMPO**), medições terrestres e informações meteorológicas, transformando dados complexos em três camadas de informação:

- Previsões precisas  
- Visualizações de inteligência que revelam tendências  
- Notícias contextuais que explicam o cenário  

O objetivo central é **reduzir a exposição da população a poluentes atmosféricos**, apoiar decisões preventivas em saúde pública com análises aprofundadas e **fomentar políticas ambientais baseadas em dados confiáveis**.  

Mais do que um app, o AeroVigil propõe **um ecossistema de dados ambientais** que fortalece decisões públicas, empodera cidadãos e amplia o acesso à ciência aplicada.

---

## Solução Proposta

### 1. O que a solução faz

- Monitora a qualidade do ar local em tempo quase real.  
- Gera previsões hiperlocais de poluição atmosférica.  
- Oferece visualizações de inteligência ambiental, revelando correlações, padrões e tendências históricas.  
- Apresenta um feed de notícias que conecta os dados de poluição a eventos do mundo real (ex: queimadas, decisões políticas).  
- Emite alertas personalizados sobre mudanças na qualidade do ar e oferece recomendações de ação.  
- Permite a comparação direta entre dados de satélite e sensores terrestres.  
- Aplica um sistema de pontuação de risco conforme o perfil de saúde do usuário.

---

### 2. Como funciona

O funcionamento do **AeroVigil** é dividido em módulos que se complementam:

#### Cadastro inicial

O usuário informa seus dados básicos, localização e seleciona seu perfil de uso:

- **Padrão:** Para pessoas leigas que desejam informações simples e diretas.  
- **Avançado:** Para pesquisadores, gestores ou entusiastas que desejam acesso detalhado aos dados e modelos.

#### Coleta e integração de dados

O backend integra continuamente informações de múltiplas fontes:

- APIs da **NASA TEMPO** (dados atmosféricos de NO₂, O₃, HCHO, aerossóis).  
- Plataformas **OpenAQ** e redes locais de sensores (PM2.5, PM10).  
- Dados meteorológicos da **NASA POWER API**, **NOAA**, **INMET** e **CPTEC**.  
- Informações geoespaciais como relevo, uso do solo e densidade populacional.

#### Processamento e previsão

- Algoritmos de *machine learning* (ex: **LSTM**, **ARIMA**) e fórmulas atmosféricas são aplicados para gerar previsões de qualidade do ar entre 24 e 48 horas.  
- O sistema calcula o **Índice de Qualidade do Ar (AQI)**, traduzindo os dados em uma escala compreensível (1 a 500), com cores e recomendações de saúde.  

Categorias do AQI:  
**Boa → Perigosa** (6 níveis totais, de *Good* a *Hazardous*).

#### Visualização e alertas

- Mapas interativos coloridos com legendas intuitivas.  
- Notificações em tempo real conforme a localização e o perfil do usuário.  
- No modo avançado, é possível visualizar dados brutos, comparar séries e exportar relatórios.

#### Módulos de Inteligência e Contexto

- **Inteligência Ambiental:**  
  Sobre a camada de dados já coletada, o sistema aplica análises para gerar dashboards de inteligência — gráficos de correlação (ex: poluição vs. hora do dia), mapas de dispersão e análises de tendência.

- **Feed de Notícias:**  
  Um módulo de curadoria associa notícias de fontes confiáveis a eventos e localizações.  
  Quando os dados mostram uma anomalia (ex: pico de poluição por fumaça), o app exibe a notícia correspondente explicando a causa.

---

### 3. Benefícios da solução

- **Para cidadãos comuns:**  
  Acesso rápido à qualidade do ar, com recomendações de saúde e notícias que explicam o cenário ambiental local.  

- **Para gestores públicos:**  
  Dados validados para decisões preventivas e políticas públicas mais eficientes, apoiadas por dashboards de inteligência.  

- **Para pesquisadores:**  
  Ferramentas para análise comparativa e exploração de dados ambientais, enriquecidas com visualizações de tendências e correlações automáticas.  

- **Para a comunidade:**  
  Transparência ambiental e acesso a informações contextualizadas que promovem a educação científica e o engajamento cívico.  

---

## Sobre o satélite TEMPO e sua relevância para o AeroVigil

A missão **TEMPO** (*Tropospheric Emissions: Monitoring of Pollution*) é a espinha dorsal do projeto.  
Lançado em abril de 2023 em **órbita geoestacionária**, o TEMPO é o primeiro instrumento espacial a **medir continuamente a qualidade do ar sobre a América do Norte** a cada hora diurna.

Ele monitora o continente do Atlântico ao Pacífico, da Península de Yucatán até o Canadá, medindo poluentes na troposfera como:

- Dióxido de nitrogênio (NO₂)  
- Ozônio (O₃)  
- Formaldeído (HCHO)  
- Aerossóis  

Sua resolução espacial (**2 km/pixel N–S e 4,5 km/pixel L–O**) e frequência horária são um avanço vital para rastrear eventos dinâmicos como picos de poluição em horários de rush ou dispersão de fumaça de incêndios florestais.  

Para o **AeroVigil**, o TEMPO é a **base do sistema de previsão**, permitindo integrar medições quase em tempo real com dados de solo e meteorológicos para fornecer **alertas contextualizados**.

---

### Fontes e integração de dados NASA

- **ASDC (Atmospheric Science Data Center):**  
  Distribui gratuitamente os dados do TEMPO a partir do NASA Langley Research Center.  
  O ASDC suporta mais de 50 projetos e fornece acesso a mais de 1.000 conjuntos de dados.  

- **APIs e Acesso Programático:**  
  O acesso é feito via **Earthdata Developer Portal**, com uso de:  
  - *Earthdata Search API* (busca e descoberta)  
  - *GIBS (Global Imagery Browse Services)* (visualização interativa de imagens de satélite)

- **AQI (Air Quality Index):**  
  Ferramenta essencial para traduzir dados científicos em ações práticas para cidadãos e gestores.

- **Fontes Complementares:**  
  - **LANCE** (*Land, Atmosphere Near real-time Capability for Earth Observation*)  
  - **HLS** (*Harmonized Landsat and Sentinel-2*)

---

## Sistema de Pontuação (AQI)

| Índice (AQI) | Classificação | Cor | Ação Sugerida |
|---------------|----------------|-----|----------------|
| 1–50 | **Boa** | 🟢 Verde | Aproveite atividades ao ar livre. |
| 51–100 | **Moderada** | 🟡 Amarelo | Evite exposição prolongada se tiver alergias. |
| 101–150 | **Ruim** | 🟠 Laranja | Limite atividades externas intensas. |
| 151–200 | **Muito Ruim** | 🔴 Vermelho | Permaneça em ambientes fechados. |
| 201–500 | **Perigosa** | 🟣 Roxo | Evite sair e mantenha janelas fechadas. |
---

