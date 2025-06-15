import streamlit as st
from lotomania import (
    obter_ultimos_resultados_lotomania,
    gerar_cartelas,
    salvar_jogos_em_txt
)

st.set_page_config(page_title="🔢 Lotomania Inteligente", layout="wide")
st.title("🔢 Lotomania Inteligente com 50 Dicas Matemáticas")

st.markdown("Gere jogos otimizados com base em padrões estatísticos reais e confira com concursos oficiais.")
st.sidebar.header("🎛️ Configurações do Jogo")

qtd_concursos = st.sidebar.slider("📊 Quantos concursos deseja capturar?", 10, 1500, 100, step=10)
qtd_jogos = st.sidebar.slider("🎲 Quantos jogos deseja gerar?", 1, 500, 10)

numeros_excluir_str = st.sidebar.text_input("🚫 Números para excluir (máx. 10, separados por vírgula)", "")
numeros_excluir = []

if numeros_excluir_str:
    try:
        numeros_excluir = list(set(int(n.strip()) for n in numeros_excluir_str.split(",") if n.strip() != ""))
        if len(numeros_excluir) > 10:
            st.sidebar.error("Você pode excluir no máximo 10 dezenas.")
            numeros_excluir = []
        elif any(n < 0 or n > 99 for n in numeros_excluir):
            st.sidebar.error("Informe apenas números de 0 a 99.")
            numeros_excluir = []
    except ValueError:
        st.sidebar.error("Use apenas números separados por vírgula.")
        numeros_excluir = []

if st.button("🚀 Gerar Jogos"):
    with st.spinner("⏳ Processando..."):
        resultados = obter_ultimos_resultados_lotomania(qtd_concursos)
        if not resultados:
            st.error("Erro ao capturar concursos. Verifique sua conexão com a internet.")
        else:
            st.success(f"{len(resultados)} concursos capturados com sucesso!")

            st.subheader(f"🧮 Gerando {qtd_jogos} jogos com até 10 exclusões aplicadas")
            jogos = gerar_cartelas(qtd_jogos, numeros_excluir)

            for idx, jogo in enumerate(jogos, 1):
                st.markdown(f"**Jogo {idx:03}:** " + ", ".join(f"{n:02}" for n in jogo))

            salvar_jogos_em_txt(jogos, "jogos_lotomania.txt")
            with open("jogos_lotomania.txt", "rb") as f:
                st.download_button("📥 Baixar Jogos em TXT", f, file_name="jogos_lotomania.txt")

    st.markdown("---")
    st.markdown("🧠 Baseado nas 50 dicas estatísticas reais da Lotomania.")
    st.markdown("👤 Desenvolvido por: **SAM ROCK**")