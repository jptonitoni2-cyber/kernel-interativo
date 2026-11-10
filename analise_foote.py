import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuração da página do Streamlit
st.set_page_config(page_title="Interpretador da Novidade de Foote", layout="wide")

st.title(" Interpretador Interativo: Novidade de Foote")
st.markdown("""
Este aplicativo foi desenvolvido para explicar a estrutura, dinâmica e formulação matemática do 
**Gráfico de Novidade de Foote**, mapeando mudanças estruturais ao longo do tempo.
""")

# --- EQUAÇÕES EM DESTAQUE ---
st.info("###  Formulação Matemática Utilizada")
st.latex(r"N(i, w) = \sum_{m=-w}^{w} \sum_{n=-w}^{w} K_w(m, n) \cdot D(i + m, i + n)")
st.latex(r"K_w(m, n) = -\text{sinal}(m) \cdot \text{sinal}(n) \cdot \exp\left( -\frac{m^2 + n^2}{2\sigma^2} \right) \quad \text{com } \sigma = 0.4 \cdot w")
st.caption("Nota: $K_w(m, n) = 0$ sempre que $m = 0$ ou $n = 0$.")

# --- ABAS PARA ORGANIZAÇÃO DO CONTEÚDO ---
tab1, tab2, tab3 = st.tabs([" O Gráfico de Cúpula", " Teste de Permutação (Linhas Pretas)", "🕹️ Simulador de Parâmetros"])

# Gerando dados sintéticos realistas para a simulação de 1960 a 2010
anos = np.arange(1960, 2010.25, 0.25)
T = len(anos)
w_valores = np.linspace(1, 10, 20)

# Construindo a Matriz de Novidade Sintética N(i, w) com formato de cúpula
N_matriz = np.zeros((len(w_valores), T))
for idx_w, w_val in enumerate(w_valores):
    # Definindo a restrição de borda da cúpula (precisa de w anos de cada lado)
    for idx_i, ano in enumerate(anos):
        if (ano >= 1960 + w_val) and (ano <= 2010 - w_val):
            # Adicionando picos simulados nos anos históricos: 1963, 1982 e 1991
            pico1 = 1.2 * np.exp(-((ano - 1963.75) / (0.15 * w_val))**2)
            pico2 = 2.0 * np.exp(-((ano - 1982.75) / (0.08 * w_val))**2)
            pico3 = 2.5 * np.exp(-((ano - 1991.00) / (0.06 * w_val))**2)
            
            # Unindo os picos com um ruído de fundo menor nas janelas grandes
            N_matriz[idx_w, idx_i] = (pico1 + pico2 + pico3) * (1.1 - 0.05 * w_val) + np.random.uniform(0, 0.1)
        else:
            N_matriz[idx_w, idx_i] = np.nan  # Fora da cúpula de dados disponíveis

with tab1:
    st.subheader("Entendendo as Dimensões e Cores do Gráfico")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Plotando o mapa de contorno interativo (Cúpula de Foote)
        fig = go.Figure(data=go.Contour(
            z=N_matriz, x=anos, y=w_valores,
            colorscale='Jet', contours_coloring='heatmap',
            connectgaps=False, hoverongaps=False, line_width=0
        ))
        
        # Adicionando linhas tracejadas verticais para marcar os picos históricos
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
        * **Formato de Cúpula:** Observe como o gráfico encolhe no topo. Para analisar com uma janela de $w=10$ anos, o sistema precisa de dados de 10 anos antes e depois, limitando o cálculo entre 1970 e 2000.
        * **Gradiente de Cores:** Transiciona do **Azul** (estabilidade/sem mudanças) ao **Marrom/Vermelho** (picos de novidade extrema).
        * **Linhas Tracejadas:** Indicam as maiores rupturas estruturais detectadas pelo modelo (fim de 1963, fim de 1982 e início de 1991).
        """)

with tab2:
    st.subheader("Significado Estatístico das Linhas Pretas (0.05; 0.01; 0.001)")
    st.markdown("""
    As linhas pretas horizontais do gráfico original representam limites calculados por um **Teste de Permutação** (com 1.000 embaralhamentos dos trimestres):
    
    1. **Significância:** Estar acima da linha indica que a mudança detectada é real e não fruto do acaso.
    2. **O Fenômeno do 'Afundamento' (1983 e 1991):** Nos anos de 1982/1983 e 1991, as linhas de corte estatístico afundam drasticamente no gráfico vertical. 
    
    * **Por que isso acontece?** A transição estrutural nesses períodos foi tão forte e evidente que mesmo janelas minúsculas (de cerca de apenas 2 anos de largura) conseguiram atingir relevância estatística máxima ($p < 0.001$).
    """)

with tab3:
    st.subheader("Simulação Dinâmica por Trimestre")
    ano_alvo = st.slider("Selecione o ano central (i) para inspecionar:", min_value=1965.0, max_value=2005.0, value=1982.75, step=0.25)
    
    # Filtrando dinamicamente os valores de novidade para o ano arrastado no slider
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
