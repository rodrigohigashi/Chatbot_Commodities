# Importação das bibliotecas necessárias
import json
import yfinance as yf
import pandas as pd
import warnings
import re
import plotly.graph_objects as go 

import openai
from dotenv import load_dotenv, find_dotenv

# Configuração de ambiente e cliente OpenAI + supressão de avisos
warnings.filterwarnings("ignore", category=FutureWarning)  # suprimir avisos

_ = load_dotenv(find_dotenv())

client = openai.Client()

# Dicionários de suporte: mapeamento de commodities e períodos de tempo

# Mapeia nomes em português para os códigos das commodities usadas no Yahoo Finance
commodities = {
    'ouro': 'GC=F',
    'prata': 'SI=F',
    'petróleo': 'CL=F',
    'milho': 'ZC=F',
    'trigo': 'ZW=F',
    'café': 'KC=F',
    'cacau': 'CC=F',
    'soja': 'ZS=F',
    'algodão': 'CT=F',
    'aveia': 'ZO=F'
}

# Tradução de períodos em linguagem natural para o formato esperado pela API
traducoes_periodo = {
    "1 dia": "1d",
    "1 semana": "7d",
    "1 mês": "1mo",
    "2 meses": "2mo",
    "3 meses": "3mo",
    "6 meses": "6mo",
    "1 ano": "1y"
}

# Inversão do dicionário para permitir validação e exibição amigável
periodos_validos = {v: k for k, v in traducoes_periodo.items()}


# Função que retorna a cotação mais recente de uma commodity para o período informado
def retorna_cotacao_commodity(commodity, periodo):
    ticker = commodities.get(commodity.lower())  # Obtém o ticker correspondente

    if not ticker:
        return f"Commodity '{commodity}' não encontrada. Tente uma das opções: {', '.join(commodities.keys())}."

    # Define período padrão e valida entrada
    periodo = periodo.lower() if periodo else '1mo'
    if periodo not in periodos_validos:
        return f"Período '{periodo}' não é válido. Tente um dos seguintes: {', '.join(periodos_validos.keys())}."

    # Busca histórico de preços da commodity
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(period=periodo)['Close']

    if hist.empty:
        return f"Não foram encontrados dados para {commodity} no período {periodo}."

    ultima_cotacao = hist[-1]

    # Ajusta valor de commodities em centavos (ex: soja)
    if ticker == 'ZS=F':
        ultima_cotacao /= 100

    return f'A cotação do {commodity} mais recente é de ${ultima_cotacao:.2f}'


#######################################################################################

# Gera o gráfico de candlestick com estatísticas e possíveis alertas de preço para uma commodity
def grafico_candlestick(commodity, periodo='1mo'):
    ticker = commodities.get(commodity.lower())
    if not ticker:
        return f"Commodity '{commodity}' não encontrada."

    try:
        hist = yf.Ticker(ticker).history(period=periodo)
        if hist.empty:
            return f"Não foram encontrados dados para {commodity} no período {periodo}."

        hist.index = pd.to_datetime(hist.index)

        # Verifica colunas essenciais
        if any(col not in hist.columns or hist[col].isnull().all() for col in ['Open', 'High', 'Low', 'Close']):
            return f"Dados insuficientes para gerar o gráfico de {commodity} ({periodo})."

        periodo_legivel = periodos_validos.get(periodo, periodo)

        # Gráfico base
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close']
        )])

        # Estatísticas
        media = hist['Close'].mean()
        minimo = hist['Close'].min()
        maximo = hist['Close'].max()
        desvio_padrao = hist['Close'].std()
        q1 = hist['Close'].quantile(0.25)
        inicio, fim = hist['Close'].iloc[0], hist['Close'].iloc[-1]
        variacao = ((fim - inicio) / inicio) * 100

        anotacao = (
            f"Média: {media:.2f} | Mínimo: {minimo:.2f} | Máximo: {maximo:.2f} | "
            f"Desvio padrão: {desvio_padrao:.2f} | Variação: {variacao:.2f}%"
        )

        # Layout
        fig.update_layout(
            title=dict(
                text=f'Gráfico Candlestick de {commodity.capitalize()} ({periodo_legivel})',
                x=0.5, font=dict(size=22)
            ),
            xaxis_title='Data',
            yaxis_title='Preço (USD)',
            xaxis_rangeslider_visible=False,
            margin=dict(t=80, b=250, l=50, r=50),
            plot_bgcolor='white',
            autosize=True
        )

        # Anotação com estatísticas
        fig.add_annotation(
            text=anotacao,
            xref="paper", yref="paper",
            x=0.5, y=-0.4,
            showarrow=False,
            font=dict(size=12)
        )

        # Alerta
        alerta_texto = ""
        if fim <= q1:
            alerta_texto = f"⚠️ Alerta: o preço de fechamento mais recente está abaixo ou igual ao primeiro quartil (Q1 = {q1:.2f})."
            fig.add_annotation(
                text=alerta_texto,
                xref="paper", yref="paper",
                x=0.5, y=-0.5,
                showarrow=False,
                font=dict(size=14, color="red")
            )

        fig.show(block=False)

        return f"Gráfico de {commodity} no período {periodo_legivel} exibido com sucesso.\n{anotacao}{alerta_texto}"

    except Exception as e:
        print(f"[DEBUG] Erro capturado: {e}")
        if 'rate limit' in str(e).lower():
            return "Limite de requisições atingido na API de dados financeiros. Tente novamente mais tarde."
    import traceback
    traceback.print_exc()
    return f"Erro ao gerar gráfico: {type(e).__name__} - {e}"


    
##############################################################################################

# Tools (se houver ferramentas específicas sendo usadas no código)
tools = [
    {
        "type": "function",
        "function": {
            "name": "retorna_cotacao_commodity",
            "description": "Retorna a cotação atual de uma commodity como ouro, prata, petróleo, café ou milho.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commodity": {
                        "type": "string",
                        "description": "Nome da commodity (ex: petróleo, ouro, milho, café)"
                    },
                    "periodo": {
                        "type": "string",
                        "description": "Período para exibir os dados, como '1d', '5d', '1mo', '3mo', '6mo', '1y', ou '5y'"
                    }
                },
                "required": ["commodity", "periodo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "grafico_candlestick",
            "description": "Gera um gráfico de velas (candlestick) para uma commodity em um período determinado, com estatísticas e alerta de preço.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commodity": {
                        "type": "string",
                        "description": "Nome da commodity (ex: petróleo, ouro, milho, café)"
                    },
                    "periodo": {
                        "type": "string",
                        "description": "Período para exibir os dados, como '1d', '5d', '1mo', '3mo', '6mo', '1y', ou '5y'"
                    }
                },
                "required": ["commodity"]
            }
        }
    }
]

# Dicionário de funções que o agente pode chamar
funcoes_disponiveis = {
    "retorna_cotacao_commodity": retorna_cotacao_commodity,
    "grafico_candlestick": grafico_candlestick
}
 
#########################################################################

# Função que interage com a API da OpenAI e gera a resposta do chatbot
def gera_texto(mensagens, forcar_tool=False):
    if forcar_tool:
        escolha_tool = {"type": "function", "function": {"name": "grafico_candlestick"}}
    else:
        escolha_tool = 'auto'

    resposta = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        messages=mensagens,
        tools=tools,
        tool_choice=escolha_tool
    )

    resposta_primaria = resposta.choices[0].message
    mensagens.append(resposta_primaria)


    if resposta_primaria.tool_calls:
        for call in resposta_primaria.tool_calls:
            nome_funcao = call.function.name
            argumentos = json.loads(call.function.arguments)

            retorno = funcoes_disponiveis[nome_funcao](**argumentos)

            mensagens.append({
                'role': 'tool',
                'tool_call_id': call.id,
                'name': nome_funcao,
                'content': retorno
            })

        resposta_final = client.chat.completions.create(
            model='gpt-3.5-turbo-0125',
            messages=mensagens
        )
        mensagens.append(resposta_final.choices[0].message)

    return mensagens


if __name__ == '__main__':
    print('Bem-vindo ao ChatBot de Commodities.')
    mensagens = []

    while True:
        input_usuario = input('User: ')
        mensagens.append({'role': 'user', 'content': input_usuario})

        # Aqui você pode mudar para True temporariamente se quiser forçar a execução da função
        mensagens = gera_texto(mensagens, forcar_tool=False)

        # Verifica se a última mensagem é do assistente e a exibe
        if mensagens and mensagens[-1].role == 'assistant' and hasattr(mensagens[-1], 'content'):
            print(f"Assistant: {mensagens[-1].content}")

