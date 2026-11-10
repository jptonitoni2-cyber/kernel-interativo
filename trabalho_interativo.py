import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuração da página do Streamlit
st.set_page_config(page_title="Seção Interativa: Análise de Kernel", layout="wide")

st.title("Visualizador Interativo do Kernel $K(m, n)$")
st.markdown("""
Esta seção interativa permite explorar o comportamento do kernel definido pela equação:
$$K(m, n) = -\\text{sinal}(m) \\cdot \\text{sinal}(n) \\cdot \\exp\\left( -\\frac{m^2 + n^2}{2\\sigma^2} \\right)$$
onde $\\sigma = 0.4 \\cdot w$.
""")

# Barra lateral para controle dos parâmetros
st.sidebar.header("Parâmetros do Filtro")
w = st.sidebar.slider("Valor de w (Largura)", min_value=0.5, max_value=10.0, value=2.5, step=0.1)
grid_size = st.sidebar.slider("Tamanho da Janela (Grid)", min_value=3, max_value=21, value=11, step=2)

# Cálculos matemáticos
sigma = 0.4 * w

# Criando a grade de coordenadas (m, n) centralizada na origem
half_grid = grid_size // 2
m_range = np.arange(-half_grid, half_grid + 1)
n_range = np.arange(-half_grid, half_grid + 1)
M, N = np.meshgrid(m_range, n_range)

# Aplicando a fórmula do Kernel K(m, n)
sinal_M = np.sign(M)
sinal_N = np.sign(N)
gaussiano = np.exp(-(M**2 + N**2) / (2 * (sigma**2)))
K = -sinal_M * sinal_N * gaussiano

# Layout em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Visualização Matriz (Heatmap)")
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=K, x=m_range, y=n_range,
        colorscale='RdBu', zmin=-1, zmax=1
    ))
    fig_heatmap.update_layout(xaxis_title="m", yaxis_title="n", height=450)
    st.plotly_chart(fig_heatmap)

with col2:
    st.subheader("Superfície 3D Interativa")
    fig_3d = go.Figure(data=[go.Surface(
        z=K, x=m_range, y=n_range,
        colorscale='RdBu', cmin=-1, cmax=1
    )])
    fig_3d.update_layout(
        scene=dict(xaxis_title='m', yaxis_title='n', zaxis_title='K(m,n)'),
        height=450
    )
    st.plotly_chart(fig_3d)

# Exibição dos valores numéricos da matriz gerada
st.subheader("Valores Numéricos da Matriz do Kernel")
st.dataframe(np.round(K, 4))
