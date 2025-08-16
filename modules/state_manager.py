# modules/state_manager.py
import streamlit as st
from .data_persistence import carregar_historico

# Dicionário de apostas especiais com os números
APOSTAS_ESPECIAIS = {
    "Viz 0": [22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25,17,34],
    "Viz 23": [31,14,20,1,33,16,24,5,10,23,8,30,11,36,13,27,6,34,17],
    "viz 22": [0,26,3,35,12,28,7,29,18,22,9,31,14,20,1,33,16,24,5],
    "viz 34": [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10],
    "viz 1 e 2": [10,5,24,16,33,1,20,14,31,9,22,32,15,19,4,21,2,25,17,34,6,27],
    "viz 1 29 17":[12,28,7,29,18,22,9,31,14,20,1,33,16,24,21,2,25,17,34,6,27],
    "preto": [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
    "par": list(range(2, 37, 2)),
    "impar": list(range(1, 37, 2)),
    "1-18": list(range(1, 19)),
    "19-36": list(range(19, 37))
}

def inicializar_estado():
    """
    Inicializa todas as variáveis de estado da sessão.
    """
    if 'saldo' not in st.session_state:
        st.session_state.saldo = 200.00
    if 'apostas_ativas' not in st.session_state:
        # Dicionário para armazenar as apostas, exemplo: {numero: valor_total_apostado}
        st.session_state.apostas_ativas = {}
    if 'historico_jogadas' not in st.session_state:
        # Lista para armazenar o histórico de cada rodada
        st.session_state.historico_jogadas = []

def adicionar_aposta(numero, valor):
    """
    Adiciona uma aposta a um número e atualiza o saldo.
    """
    if st.session_state.saldo >= valor:
        st.session_state.apostas_ativas[numero] = st.session_state.apostas_ativas.get(numero, 0) + valor
        st.session_state.saldo -= valor
        return True
    else:
        st.warning("Saldo insuficiente para realizar esta aposta.")
        return False

def adicionar_aposta_especial(aposta_especial, valor_unitario):
    """
    Adiciona uma aposta especial (ex: Voisins) e atualiza o saldo.
    """
    numeros = APOSTAS_ESPECIAIS.get(aposta_especial, [])
    custo_total = len(numeros) * valor_unitario

    if st.session_state.saldo >= custo_total:
        for numero in numeros:
            st.session_state.apostas_ativas[numero] = st.session_state.apostas_ativas.get(numero, 0) + valor_unitario
        st.session_state.saldo -= custo_total
        return True
    else:
        st.warning(f"Saldo insuficiente para aposta {aposta_especial}. Custo total: R$ {custo_total:.2f}")
        return False

def resetar_apostas():
    """
    Limpa todas as apostas ativas.
    """
    st.session_state.apostas_ativas = {}