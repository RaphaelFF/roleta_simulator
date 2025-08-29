# app.py
import streamlit as st
import pandas as pd

# Importa as funções dos nossos módulos
from modules.gerenciador_estado import inicializar_estado, adicionar_aposta, adicionar_aposta_simples, adicionar_aposta_especial, resetar_apostas
from modules.logica_roleta import processar_jogada
from modules.componentes_interface import renderizar_mesa_de_apostas
from modules.persistencia_dados import gerar_relatorio_download

# --- Configuração Inicial e Gerenciamento de Estado ---
st.set_page_config(layout="wide", page_title="Simulador de Roleta Europeia")
inicializar_estado()

# --- Callbacks para as Ações ---
def callback_adicionar_aposta(numero):
    """Callback para adicionar uma aposta individual."""
    valor_aposta = st.session_state.get('valor_por_aposta', 0.5)
    adicionar_aposta(int(numero), valor_aposta)

def callback_adicionar_aposta_simples(aposta_simples):
    """Callback para adicionar uma aposta simples."""
    valor_aposta = st.session_state.get('valor_por_aposta', 0.5)
    adicionar_aposta_simples(aposta_simples, valor_aposta)

def callback_adicionar_aposta_especial(aposta_especial):
    """Callback para adicionar uma aposta especial."""
    valor_aposta = st.session_state.get('valor_por_aposta', 0.5)
    adicionar_aposta_especial(aposta_especial, valor_aposta)

def callback_limpar_apostas():
    """Callback para limpar todas as apostas."""
    resetar_apostas()
    st.rerun()

# --- Layout da Página Principal ---
st.title("Simulador de Roleta Europeia")
st.subheader("Simule suas estratégias e gerencie seu saldo")

# Gerenciamento de Saldo na barra lateral
st.sidebar.subheader("Gerenciamento de Saldo")
st.sidebar.metric("Saldo Atual", f"R$ {st.session_state.saldo:.2f}")

# Exibe o lucro acumulado diretamente da variável de estado
st.sidebar.metric("Lucro Total Acumulado", f"R$ {st.session_state.lucro_acumulado:.2f}")

# Adicionar/Remover fundos
valor_ajuste = st.sidebar.number_input("Adicionar ou Remover Fundos", min_value=-1000.0, max_value=1000.0, step=10.0, value=0.0, format="%.2f")
if st.sidebar.button("Atualizar Saldo"):
    st.session_state.saldo += valor_ajuste
    st.rerun()

# --- Interface da Mesa de Apostas ---
valor_aposta = st.number_input("Valor por aposta", min_value=0.5, max_value=500.0, value=0.5, step=0.5, format="%.2f", key="valor_por_aposta")
renderizar_mesa_de_apostas(callback_adicionar_aposta, callback_adicionar_aposta_simples, callback_adicionar_aposta_especial, valor_aposta)

# Exibindo as apostas ativas
if st.session_state.apostas_ativas:
    st.write("---")
    st.markdown("**Apostas Ativas:**")
    apostas_df = pd.DataFrame(st.session_state.apostas_ativas.items(), columns=['Número', 'Valor Total'])
    st.dataframe(apostas_df, use_container_width=True, hide_index=True)

    # Botão para limpar apostas com callback
    st.button("Limpar todas as apostas", on_click=callback_limpar_apostas)

# --- Processamento da Jogada ---
st.write("---")
st.subheader("Processar Jogada")
numero_sorteado = st.number_input("Digite o número sorteado no cassino", min_value=0, max_value=36, value=0)

if st.button("Confirmar Resultado", type="primary"):
    processar_jogada(numero_sorteado)
    st.rerun()

# --- Histórico e Relatório ---
st.write("---")
st.subheader("Histórico de Jogadas")
if st.session_state.historico_jogadas:
    df_historico = pd.DataFrame(st.session_state.historico_jogadas)
    st.dataframe(df_historico.tail(20), use_container_width=True, hide_index=True)
    gerar_relatorio_download()

else:
    st.info("Nenhuma jogada registrada ainda.")