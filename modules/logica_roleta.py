# modules/logica_roleta.py
from .gerenciador_estado import APOSTAS_ESPECIAIS, resetar_apostas
import streamlit as st
from .persistencia_dados import salvar_historico
import time

# Mapeamento para apostas de colunas, dúzias, par/ímpar, etc.
# Embora o foco inicial seja apenas em números, já deixamos a estrutura para expansão.
APOSTAS_ADICIONAIS = {
    "vermelho": [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36],
    "preto": [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35],
    "par": list(range(2, 37, 2)),
    "impar": list(range(1, 37, 2)),
    "1-18": list(range(1, 19)),
    "19-36": list(range(19, 37))
}

def obter_apostas_vencedoras(numero_sorteado, apostas_ativas):
    """
    Verifica quais apostas são vencedoras com base no número sorteado.
    Retorna um dicionário de apostas vencedoras e seus valores.
    """
    vencedoras = {}

    # Aposta em número único (pagamento 35:1)
    if numero_sorteado in apostas_ativas:
        vencedoras[numero_sorteado] = apostas_ativas[numero_sorteado]

    return vencedoras

def calcular_ganhos(numero_sorteado, apostas_ativas):
    """
    Calcula o ganho total para a rodada com base nas apostas ativas,
    incluindo apostas simples.
    """
    ganhos = 0

    # Verifica apostas em número único (pagamento 35:1)
    if numero_sorteado in apostas_ativas:
        valor_apostado = apostas_ativas[numero_sorteado]
        ganhos += valor_apostado * 35

    # Verifica apostas simples (pagamento 1:1)
    for aposta, numeros in APOSTAS_ADICIONAIS.items():
        if aposta in apostas_ativas:
            if numero_sorteado in numeros:
                # Retorna o valor apostado + o ganho (1:1)
                ganhos += apostas_ativas[aposta] * 2

    # Importante: o valor das apostas individuais também é devolvido
    # Isso precisa ser tratado fora desta função para não duplicar o cálculo
    # mas a lógica aqui está correta para os ganhos brutos.

    return ganhos

def processar_jogada(numero_sorteado):
    """
    Processa uma jogada completa: calcula ganhos, atualiza saldo e histórico.
    """
    valor_total_apostado = sum(st.session_state.apostas_ativas.values())
    
    if valor_total_apostado == 0:
        st.error("Nenhuma aposta foi realizada. Por favor, faça suas apostas.")
        return

    ganhos_da_rodada = calcular_ganhos(numero_sorteado, st.session_state.apostas_ativas)
    
    # Adiciona os ganhos brutos ao saldo
    st.session_state.saldo += ganhos_da_rodada
    
    # Atualiza o lucro total acumulado
    # Adiciona o ganho BRUTO, pois a aposta já foi subtraída
    st.session_state.lucro_acumulado += ganhos_da_rodada

    # Registra a jogada no histórico (aqui o Lucro Líquido ainda é importante)
    ganho_liquido_rodada = ganhos_da_rodada - valor_total_apostado
    rodada_info = {
        'Numero Sorteado': numero_sorteado,
        'Valor Total Apostado': valor_total_apostado,
        'Ganhos Liquidos': ganho_liquido_rodada,
        'Saldo Final': st.session_state.saldo,
        'Lucro Total': st.session_state.lucro_acumulado
    }
    st.session_state.historico_jogadas.append(rodada_info)

    #salvar_historico(st.session_state.historico_jogadas)

    st.success(f"Número sorteado: **{numero_sorteado}**")
    st.info(f"Ganho na rodada: R$ {ganhos_da_rodada:.2f}")

    resetar_apostas()