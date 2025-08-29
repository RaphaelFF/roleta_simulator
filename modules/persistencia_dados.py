# modules/data_persistence.py
import streamlit as st
import pandas as pd
import os

# Nome do arquivo onde o histórico será salvo
NOME_ARQUIVO = "historico_roleta.csv"

def salvar_historico(historico):
    """
    Salva o histórico de jogadas em um arquivo CSV.
    A coluna Lucro Total já é passada pelo histórico.
    """
    if historico:
        try:
            df = pd.DataFrame(historico)
            
            # Reordena as colunas
            colunas_ordenadas = ['Numero Sorteado', 'Valor Total Apostado', 'Ganhos Liquidos', 'Saldo Final', 'Lucro Total']
            df = df[colunas_ordenadas]
            
            # Converte as colunas numéricas para o tipo inteiro para uma formatação limpa
            colunas_para_int = ['Numero Sorteado', 'Valor Total Apostado', 'Ganhos Liquidos', 'Saldo Final', 'Lucro Total']
            for coluna in colunas_para_int:
                # Usa pd.to_numeric para forçar a conversão, preenche NaN com 0 e então converte para Int64
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0)
                
            df.to_csv(NOME_ARQUIVO, index=False)
        except Exception as e:
            st.error(f"Erro ao salvar o histórico: {e}")
            st.warning("Verifique se há dados inválidos no seu histórico de jogadas.")
            # Para depuração, você pode querer exibir o DataFrame que está causando o erro
            # st.write(df)
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
        df = pd.read_csv(NOME_ARQUIVO)
        # Garante que as colunas numéricas sejam convertidas corretamente ao carregar
        colunas_para_int = ['Numero Sorteado', 'Valor Total Apostado', 'Ganhos Liquidos', 'Saldo Final']
        for coluna in colunas_para_int:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0)
        
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