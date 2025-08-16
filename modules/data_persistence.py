# modules/data_persistence.py
import streamlit as st
import pandas as pd
import os

# Nome do arquivo onde o histórico será salvo
NOME_ARQUIVO = "historico_roleta.csv"
SALDO_INICIAL = 200.00  # O saldo inicial do simulador

def salvar_historico(historico):
    """
    Salva o histórico de jogadas em um arquivo CSV, calculando o lucro total.
    """
    if historico:
        df = pd.DataFrame(historico)
        
        # Calcula o Lucro Total com base no saldo inicial
        df['Lucro Total'] = df['Saldo Final'] - SALDO_INICIAL
        
        # Reordena as colunas para que Lucro Total fique em uma posição lógica
        colunas_ordenadas = ['Numero Sorteado', 'Valor Total Apostado', 'Ganhos Liquidos', 'Saldo Final', 'Lucro Total']
        df = df[colunas_ordenadas]
        
        # Converte as colunas numéricas para o tipo inteiro para uma formatação limpa
        colunas_para_int = ['Numero Sorteado', 'Valor Total Apostado', 'Ganhos Liquidos', 'Saldo Final', 'Lucro Total']
        for coluna in colunas_para_int:
            # Use pd.to_numeric para garantir que a conversão seja segura
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
            
        df.to_csv(NOME_ARQUIVO, index=False)
    else:
        # Se o histórico estiver vazio, cria um arquivo com os cabeçalhos
        colunas = ['Numero Sorteado', 'Valor Total Apostado', 'Ganhos Liquidos', 'Saldo Final', 'Lucro Total']
        pd.DataFrame(columns=colunas).to_csv(NOME_ARQUIVO, index=False)


def carregar_historico():
    """
    Carrega o histórico de jogadas de um arquivo CSV, se ele existir.
    Retorna uma lista de dicionários.
    """
    if os.path.exists(NOME_ARQUIVO):
        df = pd.read_csv(NOME_ARQUIVO, dtype={
            'Numero Sorteado': 'float',
            'Valor Total Apostado': 'float',
            'Ganhos Liquidos': 'float',
            'Saldo Final': 'float',
            'Lucro Total': 'float'
        })
        return df.to_dict('records')
    else:
        return []


def gerar_relatorio_download():
    """
    Gera um botão de download para o arquivo CSV do histórico.
    """
    if os.path.exists(NOME_ARQUIVO):
        with open(NOME_ARQUIVO, "r") as f:
            st.download_button(
                label="Download Relatório CSV",
                data=f,
                file_name="relatorio_roleta.csv",
                mime="text/csv",
            )