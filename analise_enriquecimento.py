import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import hypergeom
import plotly.express as px

# Configuracao da pagina do Streamlit
st.set_page_config(page_title="Enriquecimento de Tags (GeneMerge)", layout="wide")

st.title("Dando Nome as Mudancas: Enriquecimento de Tags via GeneMerge")
st.markdown("""
Este aplicativo interativo demonstra como a analise de enriquecimento do **GeneMerge (Castillo-Davis; Hartl, 2003)**, 
uma tecnica originaria da genetica, foi adaptada para mapear a evolucao musical. Aqui, os **'genes' viram musicas** 
e as **'funcoes genicas' viram tags de genero do Last.fm**.
""")

# --- EQUACAO PRINCIPAL ---
st.info("### Calculo Estatistico: Cauda da Distribuicao Hipergeometrica")
st.latex(r"P(X \ge k) = \sum_{i=k}^{\min(n, K)} \frac{\binom{K}{i} \binom{N - K}{n - i}}{\binom{N}{n}}")

# --- ABAS DIDATICAS ---
tab1, tab2, tab3 = st.tabs([
    "Como Operar o Simulador", 
    "Fundamentacao Teorica", 
    "Guia de Cenarios Historicos"
])

with tab1:
    st.markdown("""
    ### Guia de Operacao das Variaveis (Painel Lateral):
    Para simular o enriquecimento de uma tag e testar a significancia estatistica do grupo, ajuste os controles seguindo a lógica do modelo:
    * **N (Total do Universo):** O tamanho total do banco de dados de musicas que possuem alguma tag de genero.
    * **K (Presenca da Tag no Universo):** Quantas musicas do universo inteiro compartilham a tag especifica $t$ que voce deseja testar.
    * **n (Tamanho do Estilo):** O numero total de musicas contidas dentro do agrupamento abstrato (Estilo $s$) isolado pelo algoritmo.
    * **k (Sucessos no Estilo):** Quantas musicas dentro desse estilo especifico possuem a tag $t$.
    """)

with tab2:
    st.markdown("""
    ### Entendendo a Logica do GeneMerge:
    * **O Significado de p:** Quanto menor o valor de $p$, mais surpreendente e encontrar tantas musicas com aquela tag no estilo se a tag estivesse espalhada de forma totalmente aleatoria (ao acaso) pelo universo.
    * **Correcao Estatistica:** O GeneMerge nao avalia apenas uma tag isolada; ele corrige o valor de $p$ com base no numero total de tags simultaneamente testadas para evitar falsos positivos.
    * **A Virada de 1991:** O ajuste quadratico dos dados temporais demonstra que houve uma troca drastica de estilos no ano de 1991. A analise de enriquecimento e a ferramenta metodologica utilizada para decodificar e dar nome a quais foram os estilos envolvidos nessa transicao.
    """)

with tab3:
    st.markdown("""
    ### Como Replicar os Resultados do Artigo Cientifico:
    Utilize os controles da barra lateral para simular o comportamento proporcional verificado nas grandes transicoes:
    
    1. **Para Simular o Estilo 2 (Hip-hop / Rap):** 
       * Mantenha um $N$ alto, defina um $K$ moderado para a tag no universo. No painel, eleve o valor de $k$ em relacao ao tamanho do estilo $n$. Voce observara o valor de $p$ descer drasticamente, comprovando a forte associacao desse estilo com *hip-hop, rap, old school e gangsta rap*.
    2. **Para Simular o Estilo 13 (Hard Rock / Metal):**
       * Configure os parametros de forma que a presenca da tag dentro do estilo ($k$) seja estatisticamente desproporcional ao universo geral. Isso simula o comportamento do grupo associado a *hard rock, hair metal e metal*, que perdeu dominancia logo apos a virada de 1991.
    """)

# --- INTERFACE DE SIMULACAO (PAINEL LATERAL) ---
st.sidebar.header("Parametros do Universo Musical")
N = st.sidebar.number_input("Total de musicas com tags no universo (N)", min_value=1000, max_value=100000, value=10000, step=1000)
K = st.sidebar.slider("Total de musicas com a Tag 't' no universo (K)", min_value=10, max_value=int(N/2), value=1500)
n = st.sidebar.slider("Tamanho do Estilo analisado 's' (n)", min_value=10, max_value=2000, value=500)
k = st.sidebar.slider("Musicas do Estilo que tem a Tag 't' (k)", min_value=0, max_value=int(min(n, K)), value=120)

# Calculo do p-value usando a funcao de sobrevivencia (sf) da distribuicao hipergeometrica
p_value = hypergeom.sf(k - 1, N, K, n)

# --- EXIBICAO DE RESULTADOS ---
st.subheader("Painel de Resultados da Simulacao Atual")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Valor de p Calculado (p-value)", value=f"{p_value:.4e}" if p_value < 0.001 else f"{p_value:.4f}")
    
    if p_value < 0.001:
        st.success("Enriquecimento Altamente Significativo! (p < 0.001). A concentracao desta tag nao e fruto do acaso. Ela define com precisao a identidade deste estilo musical.")
    elif p_value < 0.05:
        st.warning("Significativo (p < 0.05). Ha indicios estatisticos de correlacao entre a tag e o estilo analisado.")
    else:
        st.error("Nao Significativo (p >= 0.05). A concentracao observada e perfeitamente compativel com o acaso.")

with col2:
    # Estruturacao do grafico comparativo
    proporcao_universo = (K / N) * 100
    proporcao_estilo = (k / n) * 100
    
    df_plot = pd.DataFrame({
        'Ambiente': ['Universo Total (Esperado)', 'Dentro do Estilo (Observado)'],
        'Concentracao da Tag (%)': [proporcao_universo, proporcao_estilo]
    })
    
    fig = px.bar(df_plot, x='Ambiente', y='Concentracao da Tag (%)', color='Ambiente',
                 text=df_plot['Concentracao da Tag (%)'].apply(lambda x: f'{x:.1f}%'))
    fig.update_layout(showlegend=False, height=320)
    st.plotly_chart(fig)

st.caption("Nota: Este modulo computa os limites exatos da cauda superior hipergeometrica em tempo real.")
