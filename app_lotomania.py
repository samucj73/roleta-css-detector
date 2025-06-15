import streamlit as st
from lotomania import (
    obter_ultimos_resultados_lotomania,
    gerar_cartelas,
    conferir_jogos,
    salvar_jogos_em_txt
)

st.set_page_config(page_title="🔢 Lotomania Inteligente", layout="wide")
st.title("🔢 Lotomania Inteligente com 50 Dicas Matemáticas")
st.markdown("Gere jogos otimizados com base em padrões estatísticos reais e confira com concursos oficiais.")

st.sidebar.header("🎛️ Configurações do Jogo")
qtd_concursos = st.sidebar.slider("Quantos concursos capturar?", min_value=10, max_value=1500, value=100, step=10)
qtd_jogos = st.sidebar.slider("Quantos cartões deseja gerar?", min_value=1, max_value=500, value=10, step=1)

if st.button("🎲 Gerar Jogos e Conferir"):
    with st.spinner("Capturando resultados e gerando jogos otimizados..."):
        resultados = obter_ultimos_resultados_lotomania(qtd_concursos)
        if not resultados:
            st.error("Erro ao capturar concursos. Verifique sua conexão com a internet.")
        else:
            st.success(f"{len(resultados)} concursos capturados com sucesso!")
            jogos = gerar_cartelas(qtd_jogos)
            st.subheader(f"📄 {qtd_jogos} Jogos Gerados:")
            for idx, jogo in enumerate(jogos, 1):
                st.markdown(f"**Jogo {idx:03}:** " + ", ".join(f"{n:02}" for n in jogo))
            st.subheader("✅ Conferência de Acertos (Último Concurso)")
            ultimo = resultados[0]
            dezenas_ult = set(ultimo["dezenas"])
            st.markdown(f"**Concurso {ultimo['concurso']}** - Números sorteados: `{', '.join(f'{d:02}' for d in dezenas_ult)}`")
            for idx, jogo in enumerate(jogos, 1):
                acertos = len(set(jogo) & dezenas_ult)
                st.markdown(f"🔍 **Jogo {idx:03}** → `{acertos}` acertos")
            salvar_jogos_em_txt(jogos, "jogos_lotomania.txt")
            with open("jogos_lotomania.txt", "rb") as f:
                st.download_button("📥 Baixar Jogos em TXT", f, file_name="jogos_lotomania.txt")

    st.markdown("---")
    st.markdown("🧠 Desenvolvido com base nas 50 dicas do e-book estatístico da Lotomania.")
    st.markdown("📘 Por: **SAM ROCK**")