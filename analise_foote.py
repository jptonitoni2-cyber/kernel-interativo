import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuracao da pagina do Streamlit
st.set_page_config(page_title="Interpretador da Novidade de Foote", layout="wide")

st.title("Interpretador Interativo: Novidade de Foote e Transicoes de Estilo")
st.markdown("""
Este aplicativo foi desenvolvido para explicar a estrutura, dinamica e formulacao matematica do 
**Grafico de Novidade de Foote**, mapeando mudancas estruturais e analises de significancia ao longo do tempo.
""")

# --- EQUACOES EM DESTAQUE ---
st.info("### Formulacao Matematica Utilizada")
st.latex(r"N(i, w) = \sum_{m=-w}^{w} \sum_{n=-w}^{w} K_w(m, n) \cdot D(i + m, i + n)")
st.latex(r"K_w(m, n) = -\text{sinal}(m) \cdot \text{sinal}(n) \cdot \exp\left( -\frac{m^2 + n^2}{2\sigma^2} \right) \quad \text{com } \sigma = 0.4 \cdot w")

# --- ABAS PARA ORGANIZACAO DO CONTEUDO ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Grafico de Cupula", 
    "Teste de Permutacao e Significancia", 
    "O Que Mudou: Modelo Quadratico (1991)",
    "Simulador de Parametros"
])

# Gerando dados sinteticos realistas para a simulacao de 1960 a 2010
anos = np.arange(1960, 2010.25, 0.25)
T = len(anos)
w_valores = np.linspace(1, 10, 20)

# Construindo a Matriz de Novidade Sintetica N(i, w) com formato de cupula
N_matriz = np.zeros((len(w_valores), T))
for idx_w, w_val in enumerate(w_valores):
    for idx_i, ano in enumerate(anos):
        if (ano >= 1960 + w_val) and (ano <= 2010 - w_val):
            pico1 = 1.2 * np.exp(-((ano - 1963.75) / (0.15 * w_val))**2)
            pico2 = 2.0 * np.exp(-((ano - 1982.75) / (0.08 * w_val))**2)
            pico3 = 2.5 * np.exp(-((ano - 1991.00) / (0.06 * w_val))**2)
            N_matriz[idx_w, idx_i] = (pico1 + pico2 + pico3) * (1.1 - 0.05 * w_val) + np.random.uniform(0, 0.1)
        else:
            N_matriz[idx_w, idx_i] = np.nan

with tab1:
    st.subheader("Entendendo as Dimensoes e Cores do Grafico")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(data=go.Contour(
            z=N_matriz, x=anos, y=w_valores,
            colorscale='Jet', contours_coloring='heatmap',
            connectgaps=False, hoverongaps=False, line_width=0
        ))
        picos_historicos = [1963.75, 1982.75, 1991.00]
        for p in picos_historicos:
            fig.add_vline(x=p, line_dash="dash", line_color="black", opacity=0.7)
            
        fig.update_layout(
            xaxis_title="Eixo Horizontal: Trimestre Central i (Tempo)",
            yaxis_title="Eixo Vertical: Meia-largura do Kernel w (Anos)",
            yaxis=dict(type='log', tickvals=[1, 2, 5, 10]),
            height=500
        )
        st.plotly_chart(fig)
        
    with col2:
        st.markdown("""
        **Guia de Leitura Rápida:**
        * **Formato de Cúpula:** Observe como o grafico encolhe no topo. Para analisar com uma janela de $w=10$ anos, o sistema precisa de dados de 10 anos antes e depois, limitando o calculo entre 1970 e 2000.
        * **Gradiente de Cores:** Transiciona do azul (estabilidade) ao marrom/vermelho (picos de novidade extrema).
        * **Pontos de Revolucao:** Marcados pelas linhas tracejadas, sao os maximos de novidade dentro de cada regiao significativa e separam as eras do conjunto de dados (Mauch et al., 2015).
        * **Referencias Visuais:** Representa graficamente a relacao entre a matriz de distancias entre trimestres (a) e a novidade de Foote para janelas de diferentes tamanhos (b).
        """)

with tab2:
    st.subheader("Analise de Significancia por Permutacao")
    st.markdown("""
    Para saber se um pico supera o acaso, testa-se a hipotese nula de que a ordem cronologica dos trimestres nao importa para a estrutura de dados:
    
    1. **Embaralhamento:** Embaralham-se ao acaso os trimestres (linhas e colunas da matriz de distancias $D$ conjuntamente).
    2. **Recalculo:** Recalcula-se o valor de $N$ para a matriz embaralhada.
    3. **Repeticao:** O processo e repetido **1.000 vezes**, gerando a distribuicao empirica de $N$ sob o efeito do acaso.
    4. **Limiares (Quantis):** Para cada tamanho de kernel, calculam-se os quantis **0,95, 0,99 e 0,999** dessa distribuicao (representados pelas linhas pretas no grafico original).
    
    ### Interpretacao dos Picos Historicos Encontrados:
    * Picos acima do quantil 0,99 sao significativos a $p < 0,01$.
    * Picos acima do quantil 0,999 sao significativos a $p < 0,001$.
    
    Na formulacao usual, o calculo do p-value e dado por:
    $$p \\approx \\frac{1 + \\text{nº de embaralhametos com } N \\ge N_{\\text{observado}}}{1 + 1000}$$
    
    Dessa forma, com 1.000 realizacoes, o menor valor de $p$ resolnivel e cerca de **0,001**.
    
    * **4º Trimestre de 1963:** Significativo com $p < 0,01$.
    * **4º Trimestre de 1982:** Significativo com $p < 0,01$.
    * **1º Trimestre de 1991:** Significativo com $p < 0,001$. Nesses momentos de forte transicao (como 1983 e 1991), as linhas estatisticas afundam porque ate mesmo janelas pequenas de cerca de 2 anos geram resultados significativos.
    """)

with tab3:
    st.subheader("O Que Mudou: Modelo de Regressao Quadratica")
    st.markdown("""
    Para compreender a dinâmica das mudancas em cada revolucao, tomam-se os **24 trimestres (6 anos) em torno do pico**. Para cada um dos 13 estilos musicais, calcula-se a fracao $f_s(t)$ de musicas pertencentes a ele naquele trimestre, aplicando o modelo quadratico:
    
    $$f_s(t) = \\beta_0 + \\beta_1 \\cdot t + \\beta_2 \\cdot t^2 + \\text{erro}$$
    
    Onde $t$ representa o tempo, $\\beta_1$ indica a tendencia linear (subida se $\\beta_1 > 0$ ou queda se $\\beta_1 < 0$) e $\\beta_2$ indica a curvatura da transicao.
    
    ### O Caso da Revolucao de 1991 (Criterio $p < 0,01$):
    A analise de enriquecimento aponta exatamente quais estilos protagonizaram a troca estrutural observada em 1991:
    """)
    
    # Criando uma tabela para apresentar os coeficientes de forma escaneavel
    dados_regressao = {
        "Estilo": ["Estilo 2", "Estilo 13", "Estilo 5"],
        "Genero Associado": ["Hip-hop, Rap, Old school, Gangsta rap", "Hard rock, Hair metal, Metal", "Outros generos em declinio"],
        "Coeficiente Linear (Beta 1)",
        "Coeficiente Quadratico (Beta 2)",
        "Significancia (p-value)",
        "Comportamento"
    }
    st.table(pd.DataFrame(dados_regressao))
    
    st.markdown("""
    * **Estilo 13:** Alem do forte declinio linear, a curvatura tambem foi estatisticamente significativa ($\\beta_2 = -0,112, p = 0,023$), indicando que a queda se acelerou ou desacelerou de forma proeminente ao longo da janela analisada.
    """)

with tab4:
    st.subheader("Simulacao Dinamica por Trimestre")
    ano_alvo = st.slider("Selecione o ano central (i) para inspecionar:", min_value=1965.0, max_value=2005.0, value=1982.75, step=0.25)
    
    idx_ano = (np.abs(anos - ano_alvo)).argmin()
    valores_w_ano = N_matriz[:, idx_ano]
    
    fig_linha = go.Figure()
    fig_linha.add_trace(go.Scatter(x=w_valores, y=valores_w_ano, mode='lines+markers', line_color='red', name='Perfil de Novidade'))
    fig_linha.update_layout(
        title=f"Perfil de Novidade N(i, w) analisado para o ano {ano_alvo}",
        xaxis_title="Meia-largura da Janela w (anos)",
        yaxis_title="Intensidade da Novidade N",
        xaxis=dict(type='log', tickvals=[1, 2, 5, 10]),
        height=400
    )
    st.plotly_chart(fig_linha)
