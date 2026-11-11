import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import hypergeom
import plotly.express as px

# Configuracao da pagina
st.set_page_config(page_title="Enriquecimento de Tags (GeneMerge)", layout="wide")

st.title("GeneMerge Aplicado a Musica: Enriquecimento de Tags")
st.markdown("""
Esta secao interativa demonstra como algoritmos de genetica sao adaptados para a musica. 
Aqui, os **'genes' viram musicas** e as **'funcoes geneticas' viram tags de genero do Last.fm**.
""")

# --- EXPLICACAO MATEMATICA E CONTEXTO ---
st.info("### Formulacao Matematica Utilizada")
st.latex(r"P(X \ge k) = \sum_{i=k}^{\min(n, K)} \frac{\binom{K}{i} \binom{N - K}{n - i}}{\binom{N}{n}}")

st.markdown("""
### Observacoes sobre a Dinamica de Mudancas:
* **Interpretacao do p-value:** Quanto menor o p, mais surpreendente e encontrar tantas musicas com aquela tag no estilo se a tag estivesse espalhada ao acaso.
* **Correcao de Multiplos Testes:** O GeneMerge usa essa distribuicao e corrige o p pelo numero de tags testadas utilizando o metodo de Bonferroni modificado.
* **Evidencias nos Estilos:** Gracas a essa abordagem, o **Estilo 2** aparece fortemente associado a generos como *hip-hop, rap, old school e gangsta rap*, enquanto o **Estilo 13** destaca-se associado a *hard rock, hair metal e metal*.
* **Transicao Historica:** O ajuste quadratico dos dados globais mostra que houve uma troca de estilos marcante no ano de 1991, e a analise de enriquecimento e a ferramenta que revela exatamente quais foram os estilos envolvidos nessa transicao.
""")

# --- INTERFACE DE SIMULACAO ---
st.sidebar.header("Parametros do Universo Musical")
N = st.sidebar.number_input("Total de musicas com tags no universo (N)", min_value=1000, max_value=100000, value=10000, step=1000)
K = st.sidebar.slider("Total de musicas que possuem a Tag 't' no universo (K)", min_value=10, max_value=int(N/2), value=1500)
n = st.sidebar.slider("Tamanho do Estilo/Grupo analisado 's' (n)", min_value=10, max_value=2000, value=500)
k = st.sidebar.slider("Musicas dentro do Estilo 's' que possuem a Tag 't' (k)", min_value=0, max_value=int(min(n, K)), value=120)

# Calculo real do p-value (cauda superior da distribuicao hipergeometrica)
p_value = hypergeom.sf(k - 1, N, K, n)

# --- EXIBICAO DE RESULTADO E SIGNIFICANCIA ---
st.subheader("Resultado do Teste Estatistico")
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Valor de p (p-value)", value=f"{p_value:.4e}" if p_value < 0.001 else f"{p_value:.4f}")
    
    if p_value < 0.001:
        st.success("Enriquecimento Altamente Significativo! (p < 0.001). Esta tag define muito bem esse estilo musical.")
    elif p_value < 0.05:
        st.warning("Significativo (p < 0.05). Ha evidencias de que o genero musical pertence ao grupo.")
    else:
        st.error("Nao Significativo (p >= 0.05). A presenca desta tag neste grupo pode ser mero acaso.")

with col2:
    # Grafico visual da proporcao esperado vs observado
    proporcao_universo = (K / N) * 100
    proporcao_estilo = (k / n) * 100
    
    df_plot = pd.DataFrame({
        'Ambiente': ['Universo Total', 'Dentro do Estilo'],
        'Percentual da Tag (%)': [proporcao_universo, proportion_estilo]
    })
    fig = px.bar(df_plot, x='Ambiente', y='Percentual da Tag (%)', color='Ambiente', 
                 text=df_plot['Percentual da Tag (%)'].apply(lambda x: f'{x:.1f}%'))
    fig.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig)

st.caption("Nota: Este modulo utiliza a biblioteca cientifica scipy para computar os coeficientes binomiais e as somatorias exatas.")
