# modules/state_manager.py
import streamlit as st
from .persistencia_dados import carregar_historico
import time

# Dicionário de apostas especiais com os números
APOSTAS_ESPECIAIS = {
    "Viz 0": [22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25,17,34],
    "Viz 23": [31,14,20,1,33,16,24,5,10,23,8,30,11,36,13,27,6,34,17],
    "viz 22": [0,26,3,35,12,28,7,29,18,22,9,31,14,20,1,33,16,24,5],
    "viz 34": [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10],
    "viz 1 e 2": [10,5,24,16,33,1,20,14,31,9,22,32,15,19,4,21,2,25,17,3,26,0]
}

def inicializar_estado():
    """
    Inicializa todas as variáveis de estado da sessão, carregando o histórico salvo.
    """
    # Adicionamos a inicialização do saldo inicial aqui
    if 'saldo_inicial' not in st.session_state:
        st.session_state.saldo_inicial = 200
        
    # Adicionamos a inicialização do lucro acumulado
    if 'lucro_acumulado' not in st.session_state:
        st.session_state.lucro_acumulado = 0.00
    
    if 'saldo' not in st.session_state:
        st.session_state.saldo = st.session_state.saldo_inicial
    
    if 'apostas_ativas' not in st.session_state:
        st.session_state.apostas_ativas = {}
    
    if 'historico_jogadas' not in st.session_state:
        # Tenta carregar o histórico salvo
        st.session_state.historico_jogadas = carregar_historico()

def adicionar_aposta(numero, valor):
    """
    Adiciona uma aposta a um número e atualiza o saldo.
    """
    if st.session_state.saldo >= valor:
        st.session_state.apostas_ativas[numero] = st.session_state.apostas_ativas.get(numero, 0) + valor
        st.session_state.saldo -= valor
        st.session_state.lucro_acumulado -= valor # **Nova regra**
        return True
    else:
        st.warning("Saldo insuficiente para realizar esta aposta.")
        return False

def adicionar_aposta_especial(aposta_especial, valor_unitario):

    numeros = APOSTAS_ESPECIAIS.get(aposta_especial, [])
    custo_total = len(numeros) * valor_unitario

    if st.session_state.saldo >= custo_total:
        for numero in numeros:
            st.session_state.apostas_ativas[numero] = st.session_state.apostas_ativas.get(numero, 0) + valor_unitario
        st.session_state.saldo -= custo_total
        st.session_state.lucro_acumulado -= custo_total # **Nova regra**
        return True
    else:
        st.warning(f"Saldo insuficiente para aposta {aposta_especial}. Custo total: R$ {custo_total:.2f}")
        return False
def adicionar_aposta_simples(aposta_simples, valor):
    """
    Adiciona uma aposta simples (vermelho/preto, par/ímpar) e atualiza o saldo.
    """
    if st.session_state.saldo >= valor:
        st.session_state.apostas_ativas[aposta_simples] = st.session_state.apostas_ativas.get(aposta_simples, 0) + valor
        st.session_state.saldo -= valor
        st.session_state.lucro_acumulado -= valor # **Nova regra**
        return True
    else:
        st.warning("Saldo insuficiente para realizar esta aposta.")
        return False

def resetar_apostas():
    st.session_state.apostas_ativas = {}
    time.sleep(2)
    st.rerun()