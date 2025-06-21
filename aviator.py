importar streamlit como st
importar numpy como np

st.set_page_config(page_title="Aviador - Entrada Segura", layout="centralizado")

st.title("ðŸŽ¯ Aviador: Analisador de Entradas Seguras")
st.write("Insira manualmente os últimos multiplicadores (valores da vela). O sistema avisará quando houver uma oportunidade segura de entrada com alvo acima de 2x.")

# Armazenamento do histórico na sessão
se "historico" não estiver em st.session_state:
    st.session_state.historico = []

# Inserção manual
novo_valor = st.text_input("Digite o valor da última rodada (ex: 1,45):")
if st.button("Adicionar"):
    tentar:
        valor = float(novo_valor.replace(",", "."))
        se valor >= 1,0:
            st.session_state.historico.insert(0, valor)
        outro:
            st.warning("Digite um valor válido acima de 1.0")
    exceto:
        st.error("Entrada inválida. Use ponto ou vérgula para decimais.")

#Exibição do histórico
st.subheader("ðŸ“œ Histórico (mais recente primeiro):")
st.write(st.session_state.historico[:30])

# Regras simples para entrada segura (exemplo básico)
def detectar_entrada_segura(hist):
    se len(hist) < 6:
        return False, "Aguardando mais dados..."

    últimos = hist[:6]
    abaixo_2x = [x para x nos últimos se x < 2,0]

    se len(abaixo_2x) >= 5 e todos(x < 1,8 para x em ultimos[:3]):
        return True, "Alerta: Padrão detectado após 5 rodadas ruinas — possível subida agora!"
    outro:
        return False, "Sem padrão seguro no momento."

# Análise e sugestão
st.subheader("ðŸ” Análise da Rodada Atual")
entrada_segura, mensagem = detectar_entrada_segura(st.session_state.historico)

se entrada_segura:
    st.success("âœ… ENTRADA SEGURA RECOMENDADA!\n" + mensagem)
outro:
    st.info("â ³ Aguarde: " + mensagem)

# Botão para limpar histórico
if st.button("Limpar histórico"):
    st.session_state.historico = []
    st.success("Histórico limpo com sucesso.")
