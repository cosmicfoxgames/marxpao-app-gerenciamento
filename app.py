import streamlit as st
import pandas as pd

# Lista inicial de pães (editável)
paes = [
    "Pão Francês", "Integral", "Multigrãos", "Vegano", "Queijo",
    "Doce", "Centeio", "Italiano", "Alho", "Milho",
    "Aveia", "Azeite", "Batata", "Recheado", "Pão de Forma", "Ciabatta"
]

# Número máximo de vendedores
MAX_VENDEDORES = 20

# Sessão de estado para nomes dos pães e vendedores
if 'paes' not in st.session_state:
    st.session_state.paes = paes
if 'vendedores' not in st.session_state:
    st.session_state.vendedores = [f"Vendedor {i+1}" for i in range(10)]
if 'estoque' not in st.session_state:
    st.session_state.estoque = {pao: 0 for pao in st.session_state.paes}
if 'vendas' not in st.session_state:
    st.session_state.vendas = {
        vendedor: {pao: 0 for pao in st.session_state.paes} for vendedor in st.session_state.vendedores
    }

st.title("Painel Central de Vendas da Padaria")

# Editar nomes dos pães
st.subheader("Editar nomes dos pães")
for i, nome in enumerate(st.session_state.paes):
    novo_nome = st.text_input(f"Pão {i+1}", value=nome, key=f"pao_{i}")
    if novo_nome != nome:
        antigo_nome = st.session_state.paes[i]
        st.session_state.paes[i] = novo_nome
        # Atualiza estoque e vendas com novo nome
        st.session_state.estoque[novo_nome] = st.session_state.estoque.pop(antigo_nome)
        for vendedor in st.session_state.vendas:
            st.session_state.vendas[vendedor][novo_nome] = st.session_state.vendas[vendedor].pop(antigo_nome)

# Editar nomes dos vendedores
st.subheader("Editar nomes dos vendedores")
for i, nome in enumerate(st.session_state.vendedores):
    novo_nome = st.text_input(f"Vendedor {i+1}", value=nome, key=f"vendedor_{i}")
    if novo_nome != nome:
        antigo_nome = st.session_state.vendedores[i]
        st.session_state.vendedores[i] = novo_nome
        st.session_state.vendas[novo_nome] = st.session_state.vendas.pop(antigo_nome)

# Editar estoque
st.subheader("Estoque de pães")
for pao in st.session_state.paes:
    st.session_state.estoque[pao] = st.slider(f"{pao} (Estoque)", 0, 50, st.session_state.estoque[pao])

# Mostrar tabela de vendas
st.subheader("Vendas")
for vendedor in st.session_state.vendedores:
    st.markdown(f"### {vendedor}")
    cols = st.columns(len(st.session_state.paes))
    for i, pao in enumerate(st.session_state.paes):
        st.session_state.vendas[vendedor][pao] = cols[i].number_input(
            f"{pao} ({vendedor})",
            min_value=0,
            max_value=50,
            value=st.session_state.vendas[vendedor][pao],
            key=f"{vendedor}_{pao}"
        )

# Mostrar resumo
df = pd.DataFrame(st.session_state.vendas).fillna(0)
st.subheader("Resumo Geral")
st.dataframe(df.style.format("{:,.0f}"))
