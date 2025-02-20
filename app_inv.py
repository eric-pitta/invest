import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime

def download_data(ticker, start_date, end_date, interval):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    return data

def price_range_frequency(data, num_bins=50):
    all_prices = pd.concat([data['High'], data['Low'], data['Open'], data['Close']])
    hist, bins = np.histogram(all_prices, bins=num_bins)
    return hist, bins

def get_tickers():
    return ['PETR4.SA - Petrobras', 'VALE3.SA - Vale', 'ITUB4.SA - Itau Unibanco',
        'BBDC4.SA - Bradesco', 'ABEV3.SA - Ambev', 'WEGE3.SA - Weg',
        'MGLU3.SA - Magazine Luiza', 'BBAS3.SA - Banco do Brasil',
        'LREN3.SA - Lojas Renner', 'CSNA3.SA - CSN', 'GGBR4.SA - Gerdau',
        'JBSS3.SA - JBS', 'HAPV3.SA - Hapvida', 'RADL3.SA - Raia Drogasil','^SPX','^BVSP','10Y=F - Juros EUA 10 Anos','AAPL - Apple Inc.', 'MSFT - Microsoft Corp.', 'GOOGL - Alphabet Inc.',
        'TSLA - Tesla Inc.', 'AMZN - Amazon.com Inc.', 'BTC-USD - Bitcoin',
        'ETH-USD - Ethereum', 'META - Meta Platforms Inc.', 'NVDA - NVIDIA Corp.',
        'BRK-B - Berkshire Hathaway', 'JNJ - Johnson & Johnson', 'WMT - Walmart Inc.',
        'V - Visa Inc.', 'JPM - JPMorgan Chase & Co.', 'PG - Procter & Gamble Co.',
        'XOM - Exxon Mobil Corp.', 'UNH - UnitedHealth Group', 'HD - The Home Depot Inc.',
        'INTC - Intel Corp.', 'PFE - Pfizer Inc.', 'CVX - Chevron Corp.', 'KO - Coca-Cola Co.',
        'PEP - PepsiCo Inc.', 'ABT - Abbott Laboratories', 'DIS - Walt Disney Co.',
        'CSCO - Cisco Systems Inc.', 'MRK - Merck & Co. Inc.', 'MCD - McDonald’s Corp.',
        'IBM - International Business Machines', 'NKE - Nike Inc.', 'GS - Goldman Sachs Group',
        'AMAT - Applied Materials Inc.', 'NFLX - Netflix Inc.', 'ADBE - Adobe Inc.',
        'CRM - Salesforce Inc.', 'PYPL - PayPal Holdings Inc.', 'AMD - Advanced Micro Devices Inc.',
        'BA - Boeing Co.', 'T - AT&T Inc.', 'GE - General Electric Co.', 'F - Ford Motor Co.',
        'GM - General Motors Co.', 'CL - Colgate-Palmolive Co.', 'LMT - Lockheed Martin Corp.',
        'CAT - Caterpillar Inc.', 'HON - Honeywell International Inc.', 'MMM - 3M Company',
        'SPY - SPDR S&P 500 ETF', 'QQQ - Invesco QQQ Trust', 'GLD - SPDR Gold Trust',
        'USO - United States Oil Fund', 'SLV - iShares Silver Trust', 'TLT - iShares 20+ Year Treasury Bond ETF',
        'BNB-USD - Binance Coin', 'XRP-USD - Ripple','ICP-USD - Internet Computer','ADA-USD - Cardano','MANA-USD - Decentraland','XVG-USD - Verge', 'SOL-USD - Solana',
        'DOGE-USD - Dogecoin', 'DOT-USD - Polkadot', 'AVAX-USD - Avalanche', 'UNI-USD - Uniswap',
        'LTC-USD - Litecoin', 'LINK-USD - Chainlink', 'XLM-USD - Stellar', 'FTT-USD - FTX Token',
        'BCH-USD - Bitcoin Cash', 'MATIC-USD - Polygon', 'XMR-USD - Monero', 'FIL-USD - Filecoin',
        'EOS-USD - EOS.IO', 'AAVE-USD - Aave', 'GC=F - Gold Futures', 'SI=F - Silver Futures',
        'CL=F - Crude Oil Futures', 'NG=F - Natural Gas Futures', 'HG=F - Copper Futures',
        'ZC=F - Corn Futures', 'ZW=F - Wheat Futures', 'ZS=F - Soybean Futures', 'LE=F - Live Cattle Futures',
        'HE=F - Lean Hogs Futures', 'CC=F - Cocoa Futures', 'KC=F - Coffee Futures', 'SB=F - Sugar Futures'
    ]


st.title('Mapeamento da Frequência de Preços de Ativos 📊')

menu = st.sidebar.selectbox("Selecione a Análise", ["Frequência Ativo Único", "Ranking Ativo Único", "Frequência Ativos Indexados", "Ranking Ativos Indexados"])

st.sidebar.header('Configurações')
ticker = st.sidebar.selectbox('Selecione o Ticker', get_tickers())
if menu in ["Frequência Ativos Indexados", "Ranking Ativos Indexados"]:
    ticker2 = st.sidebar.selectbox('Selecione o Segundo Ticker', get_tickers())
df_option = st.sidebar.selectbox('Selecione o Intervalo', ['5m', '15m', '30m', '1h', '1d'])
st.sidebar.markdown("<em>OBS: Para qualquer prazo intradiário só estão disponíveis dados dos últimos 60 dias</em>", unsafe_allow_html=True)
date_range = st.sidebar.date_input('Selecione o Período', [datetime(1990, 1, 1), datetime(2030, 12, 31)])

if st.sidebar.button('Executar Análise'):
    try:
        data = download_data(ticker.split(' - ')[0], date_range[0], date_range[1], df_option)

        if menu == "Frequência Ativo Único":
            # Gráfico de Frequência
            hist, bins = price_range_frequency(data)
            plt.figure(figsize=(14, 8))
            plt.bar(bins[:-1], hist, width=np.diff(bins), edgecolor='black', align='edge')
            plt.title(f'Frequência de Preços para {ticker}')
            plt.xlabel('Faixa de Preço')
            plt.ylabel('Frequência')
            plt.xticks(bins, [f'{x:.4f}' for x in bins], rotation=90)
            plt.grid(True)
            st.pyplot(plt)

            st.markdown("---")

            # Gráfico de Linha
            st.subheader(f'Gráfico de preço do ativo: {ticker}')
            if not data.empty:
                # Verifica se os dados estão completos
                if 'Close' in data.columns:
                    plt.figure(figsize=(14, 8))
                    plt.plot(data['Close'])
                    plt.title(f'Preço de Fechamento para {ticker}')
                    current_values = plt.gca().get_yticks() #add 
                    plt.gca().set_yticklabels(['{:.6f}'.format(x) for x in current_values]) #add
                    plt.xlabel('Data')
                    plt.ylabel('Preço de Fechamento')
                    plt.grid(True)
                    st.pyplot(plt)
                else:
                    st.warning("Dados de fechamento incompletos para gerar o gráfico de linha.")
            else:
                st.warning("Nenhum dado disponível para o período selecionado.")

        elif menu == "Ranking Ativo Único":
            hist, bins = price_range_frequency(data, num_bins=30)
            sorted_indices = np.argsort(hist)[::-1]
            sorted_hist = hist[sorted_indices]
            sorted_bins = bins[:-1][sorted_indices]
            plt.figure(figsize=(14, 8))
            plt.barh(range(len(sorted_hist)), sorted_hist, color='skyblue', edgecolor='black')
            plt.yticks(range(len(sorted_bins)), [f'{b:.4f}' for b in sorted_bins])
            plt.xlabel('Frequência')
            plt.ylabel('Faixa de Preço')
            plt.title(f'Ranking de Frequência para {ticker}')
            plt.gca().invert_yaxis()
            plt.grid(True)
            st.pyplot(plt)

        elif menu == "Frequência Ativos Indexados":
            data2 = download_data(ticker2.split(' - ')[0], date_range[0], date_range[1], df_option)
            merged_data = pd.merge(data['Close'], data2['Close'], left_index=True, right_index=True)
            index_data = merged_data.iloc[:, 0] / merged_data.iloc[:, 1]
            hist, bins = np.histogram(index_data, bins=30)

            # Gráfico de Frequência
            plt.figure(figsize=(14, 8))
            plt.bar(bins[:-1], hist, width=np.diff(bins), edgecolor='black', align='edge')
            plt.title(f'Frequência de Preços para {ticker}/{ticker2}')
            plt.xlabel('Faixa de Preço da Razão')
            plt.ylabel('Frequência')
            plt.xticks(bins, [f'{x:.7f}' for x in bins], rotation=90)
            plt.grid(True)
            st.pyplot(plt)

            st.markdown("---")

            # Gráfico de Linha da Razão
            st.subheader(f'Gráfico de preço da indexação dos ativos: {ticker}/{ticker2}')
            if not index_data.empty:
                plt.figure(figsize=(14, 8))
                plt.plot(index_data)
                plt.title(f'Razão de Preços ({ticker}/{ticker2})')
                current_values = plt.gca().get_yticks() #add recente
                plt.gca().set_yticklabels(['{:.6f}'.format(x) for x in current_values]) #add recente
                plt.xlabel('Data')
                plt.ylabel('Razão')
                plt.grid(True)
                st.pyplot(plt)
            else:
                st.warning("Nenhum dado disponível para o período selecionado.")

        elif menu == "Ranking Ativos Indexados":
            data2 = download_data(ticker2.split(' - ')[0], date_range[0], date_range[1], df_option)
            merged_data = pd.merge(data['Close'], data2['Close'], left_index=True, right_index=True)
            index_data = merged_data.iloc[:, 0] / merged_data.iloc[:, 1]
            hist, bins = np.histogram(index_data, bins=30)
            sorted_indices = np.argsort(hist)[::-1]
            sorted_hist = hist[sorted_indices]
            sorted_bins = bins[:-1][sorted_indices]
            plt.figure(figsize=(14, 8))
            plt.barh(range(len(sorted_hist)), sorted_hist, color='skyblue', edgecolor='black')
            plt.yticks(range(len(sorted_bins)), [f'{b:.7f}' for b in sorted_bins])
            plt.title(f'Ranking de Frequência para {ticker}/{ticker2}')
            plt.xlabel('Frequência')
            plt.ylabel('Faixa de Preço da Razão')
            plt.gca().invert_yaxis()
            plt.grid(True)
            st.pyplot(plt)

        st.success('Análise concluída!')
    except Exception as e:
        st.error(f'Erro: {e}')
else:
    st.info('Configure as opções e execute.')

st.sidebar.markdown("---")
st.sidebar.markdown("<em>As misericórdias do SENHOR são a causa de não sermos consumidos, porque as suas misericórdias não têm fim; renovam-se cada manhã. Grande é a tua fidelidade.</em>", unsafe_allow_html=True)
st.sidebar.markdown("<em>Lamentações 3:22-23</em>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("© Desenvolvido por Eric Pitta", unsafe_allow_html=True)