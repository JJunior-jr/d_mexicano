import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dominó Mexicano", layout="centered")

st.title("🎲 Dominó Mexicano - Gerenciador de Pontuação")

# Inicializar sessão
if "jogadores" not in st.session_state:
    st.session_state.jogadores = []
if "pontuacoes" not in st.session_state:
    st.session_state.pontuacoes = {}
if "rodada" not in st.session_state:
    st.session_state.rodada = 1
if "jogo_finalizado" not in st.session_state:
    st.session_state.jogo_finalizado = False
if "novo_nome" not in st.session_state:
    st.session_state.novo_nome = ""

# Cadastro de jogadores
with st.form("cadastro_jogadores"):
    nome = st.text_input("Nome do jogador", value=st.session_state.novo_nome)
    adicionar = st.form_submit_button("Adicionar jogador")
    if adicionar and nome:
        nome = nome.strip()
        if nome and nome not in st.session_state.jogadores:
            st.session_state.jogadores.append(nome)
            st.session_state.pontuacoes[nome] = []
            st.session_state.novo_nome = ""  # Limpa o campo
        elif nome in st.session_state.jogadores:
            st.warning("Jogador já cadastrado!")
        else:
            st.warning("Digite um nome válido.")
    else:
        st.session_state.novo_nome = nome  # Atualiza o campo se não foi adicionado

# Mostrar jogadores cadastrados
if st.session_state.jogadores:
    st.subheader("👥 Jogadores cadastrados")
    st.write(", ".join(st.session_state.jogadores))

# Registro de pontos da rodada
if st.session_state.jogadores and not st.session_state.jogo_finalizado:
    st.subheader(f"📝 Rodada {st.session_state.rodada}")
    with st.form("registro_pontos"):
        pontos = {}
        for jogador in st.session_state.jogadores:
            pontos[jogador] = st.number_input(f"Pontos de {jogador}", min_value=0, step=1, key=f"input_{jogador}")
        registrar = st.form_submit_button("Registrar rodada")
        if registrar:
            for jogador, ponto in pontos.items():
                st.session_state.pontuacoes[jogador].append(ponto)
            st.success("Rodada registrada com sucesso!")
            st.session_state.rodada += 1

# Mostrar tabela de totais após cada rodada
if st.session_state.pontuacoes:
    st.subheader("📊 Totais por jogador")
    totais = {
        jogador: sum(pontos)
        for jogador, pontos in st.session_state.pontuacoes.items()
    }
    df_totais = pd.DataFrame.from_dict(totais, orient="index", columns=["Total de Pontos"])
    st.table(df_totais.sort_values(by="Total de Pontos"))

# Finalizar jogo
if st.session_state.jogadores and not st.session_state.jogo_finalizado:
    if st.button("🏁 Finalizar jogo"):
        st.session_state.jogo_finalizado = True

# Mostrar ranking final
if st.session_state.jogo_finalizado:
    st.subheader("🏆 Ranking Final")
    df_ranking = df_totais.sort_values(by="Total de Pontos")
    st.table(df_ranking)

    vencedor = df_ranking.index[0]
    st.success(f"🎉 O vencedor é {vencedor} com {df_ranking.loc[vencedor, 'Total de Pontos']} pontos!")

# Reiniciar jogo
if st.session_state.jogo_finalizado:
    if st.button("🔄 Reiniciar jogo"):
        st.session_state.jogadores = []
        st.session_state.pontuacoes = {}
        st.session_state.rodada = 1
        st.session_state.jogo_finalizado = False
        st.session_state.novo_nome = ""