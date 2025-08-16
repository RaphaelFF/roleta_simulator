# modules/ui_components.py
import streamlit as st

# Mapeamento de cores dos números da roleta
NUMEROS_VERMELHOS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
NUMEROS_PRETOS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

def obter_estilo_numero(numero):
    """
    Retorna o estilo (cor) do número para a interface.
    """
    if numero == 0:
        return "green"
    elif numero in NUMEROS_VERMELHOS:
        return "red"
    else:
        return "black"

def renderizar_mesa_de_apostas(callback_aposta_numero, callback_aposta_especial, valor_aposta):
    """
    Renderiza a representação visual da mesa de roleta europeia com cores e layout aprimorados.
    """
    st.write("### Apostas Internas e Externas")
    
    # Coluna do Zero (0)
    col_zero = st.columns([0.1, 1, 0.1])
    col_zero[1].button("0", key=f"num_0", on_click=callback_aposta_numero, args=(0,))
    st.markdown("---")

    # Apostas nos números de 1 a 36 (em 3 colunas)
    numeros_mesa = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12],
        [13, 14, 15], [16, 17, 18], [19, 20, 21], [22, 23, 24],
        [25, 26, 27], [28, 29, 30], [31, 32, 33], [34, 35, 36]
    ]

    cols_numeros = st.columns(12)
    for col_idx, grupo_numeros in enumerate(numeros_mesa):
        with cols_numeros[col_idx]:
            for numero in grupo_numeros:
                cor_css = obter_estilo_numero(numero)
                st.button(
                    f"{numero}", 
                    key=f"num_{numero}", 
                    on_click=callback_aposta_numero, 
                    args=(numero,),
                    help=f"Apostar R$ {valor_aposta:.2f} no número {numero}",
                )
    
    # Apostas de Dúzias (1-12, 13-24, 25-36)
    st.markdown("---")

    
    # Apostas Simples (Vermelho/Preto, Par/Ímpar, 1-18/19-36)
    st.markdown("---")
    st.write("#### Apostas Simples")
    cols_simples = st.columns(6)
    cols_simples[0].button("1-18", key="1_18", on_click=callback_aposta_especial, args=("1-18",))
    cols_simples[1].button("Par", key="par", on_click=callback_aposta_especial, args=("par",))
    cols_simples[2].button("🔴", key="vermelho", on_click=callback_aposta_especial, args=("vermelho",))
    cols_simples[3].button("⚫", key="preto", on_click=callback_aposta_especial, args=("preto",))
    cols_simples[4].button("Ímpar", key="impar", on_click=callback_aposta_especial, args=("impar",))
    cols_simples[5].button("19-36", key="19_36", on_click=callback_aposta_especial, args=("19-36",))

    # Apostas Especiais (Voisins, Tiers, Orphelins)
    st.markdown("---")
    st.write("#### Apostas Especiais (Call Bets)")
    col_calls = st.columns(6)
    if col_calls[0].button("Viz 0", key="Viz 0", on_click=callback_aposta_especial, args=("Viz 0",)):
        pass
    if col_calls[1].button("Viz 23", key="Viz 23", on_click=callback_aposta_especial, args=("Viz 23",)):
        pass
    if col_calls[2].button("Viz 22", key="Viz 22", on_click=callback_aposta_especial, args=("viz 22",)):
        pass
    if col_calls[3].button("Viz 34", key="Viz 34", on_click=callback_aposta_especial, args=("viz 34",)):
        pass
    if col_calls[4].button("Viz 1 e 2", key="Viz 1 e 2", on_click=callback_aposta_especial, args=("viz 1 e 2",)):
        pass
    if col_calls[5].button("Viz 1 29 17", key="Viz 1 29 17", on_click=callback_aposta_especial, args=("viz 1 29 17",)):
        pass