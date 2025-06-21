import streamlit as st
import numpy as np # Although numpy isn't strictly used in the current logic, keeping it in case you expand

st.set_page_config(page_title="Aviador - Entrada Segura", layout="centered")

st.title("🎯 Aviador: Analisador de Entradas Seguras")
st.write("Insira manualmente os últimos multiplicadores (valores da vela). O sistema avisará quando houver uma oportunidade segura de entrada com alvo acima de 2x.")

# Initialize history in session state if it doesn't exist
if "historico" not in st.session_state:
    st.session_state.historico = []

# Manual input for new values
novo_valor = st.text_input("Digite o valor da última rodada (ex: 1.45):")

if st.button("Adicionar"):
    try:
        # Replace comma with dot for decimal conversion and convert to float
        valor = float(novo_valor.replace(",", "."))
        if valor >= 1.0:
            # Insert at the beginning to keep the most recent at the top
            st.session_state.historico.insert(0, valor)
        else:
            st.warning("Digite um valor válido acima de 1.0.")
    except ValueError: # Catch specific ValueError for invalid float conversion
        st.error("Entrada inválida. Use ponto ou vírgula para decimais.")

# Display history
st.subheader("📚 Histórico (mais recente primeiro):")
# Displaying up to 30 entries for readability
st.write(st.session_state.historico[:30])

# Simple rules for safe entry (basic example)
def detectar_entrada_segura(hist):
    if len(hist) < 6:
        return False, "Aguardando mais dados para análise..."

    ultimos = hist[:6] # Get the last 6 entries
    abaixo_2x = [x for x in ultimos if x < 2.0]

    # Rule: If 5 or more of the last 6 are below 2x AND the last 3 are below 1.8x
    if len(abaixo_2x) >= 5 and all(x < 1.8 for x in ultimos[:3]):
        return True, "Alerta: Padrão detectado após 5 rodadas com valores baixos — possível subida agora!"
    else:
        return False, "Sem padrão seguro no momento. Continue monitorando."

# Analysis and suggestion
st.subheader("🔍 Análise da Rodada Atual")
entrada_segura, mensagem = detectar_entrada_segura(st.session_state.historico)

if entrada_segura:
    st.success("✅ ENTRADA SEGURA RECOMENDADA!\n" + mensagem)
else:
    st.info("🕒 Aguarde: " + mensagem)

# Button to clear history
if st.button("Limpar histórico"):
    st.session_state.historico = []
    st.success("Histórico limpo com sucesso.")
