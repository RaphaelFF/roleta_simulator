# modules/roulette_logic.py
from .gerenciador_estado import APOSTAS_ESPECIAIS, resetar_apostas
import streamlit as st
from .persistencia_dados import salvar_historico

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

    # Para apostas especiais, verificamos se o número sorteado faz parte de algum dos conjuntos
    # Essa parte da lógica é importante caso expandamos o sistema para permitir apostas
    # em Voisins, Tiers, etc. como um único clique que aposta múltiplos chips.
    # No nosso caso, como a aposta já é "desmembrada" em números individuais,
    # esta etapa é mais para referência futura e para apostas que cobrem múltiplos números.

    return vencedoras

def calcular_ganhos(numero_sorteado, apostas_ativas):
    """
    Calcula o ganho total para a rodada com base nas apostas ativas.
    """
    ganhos = 0
    
    # Ganhos de aposta em número único (35:1)
    if numero_sorteado in apostas_ativas:
        valor_apostado = apostas_ativas[numero_sorteado]
        ganhos += valor_apostado * 35
        # O valor da aposta inicial é devolvido no saldo
        ganhos += valor_apostado
    
    # Poderíamos adicionar aqui a lógica para outros tipos de apostas,
    # como Split, Street, etc. para futuro.

    return ganhos

def processar_jogada(numero_sorteado):
    """
    Processa uma jogada completa: calcula ganhos, atualiza saldo e histórico.
    """
    # Aposta total para a rodada
    valor_total_apostado = sum(st.session_state.apostas_ativas.values())
    
    # Se não houver apostas, a jogada não tem custo
    if valor_total_apostado == 0:
        st.error("Nenhuma aposta foi realizada. Por favor, faça suas apostas.")
        return

    ganhos_da_rodada = calcular_ganhos(numero_sorteado, st.session_state.apostas_ativas)

    # Adiciona os ganhos ao saldo
    st.session_state.saldo += ganhos_da_rodada
    
    # Calcula o lucro total acumulado
    lucro_total_acumulado = st.session_state.saldo - st.session_state.saldo_inicial
    # Registra a jogada no histórico
    rodada_info = {
        'Numero Sorteado': numero_sorteado,
        'Valor Total Apostado': valor_total_apostado,
        'Ganhos Liquidos': ganhos_da_rodada - valor_total_apostado,
        'Saldo Final': st.session_state.saldo,
        'Lucro Total': lucro_total_acumulado # Adicionamos o lucro total aqui
    }
    st.session_state.historico_jogadas.append(rodada_info)
   



    # **Salva o histórico em arquivo após cada jogada**
    salvar_historico(st.session_state.historico_jogadas)

    # Exibe o resultado para o usuário
    st.success(f"Número sorteado: **{numero_sorteado}**")
    st.info(f"Ganho na rodada: R$ {ganhos_da_rodada:.2f}")


    # Limpa as apostas para a próxima rodada
    resetar_apostas()