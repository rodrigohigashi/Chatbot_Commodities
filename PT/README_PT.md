🤖 Chatbot para Análise de Commodities com OpenAI e Yahoo Finance 📈
Sobre o projeto

Um sistema conversacional que permite analisar commodities financeiras como ouro, petróleo e café utilizando linguagem natural, dados históricos e geração automática de gráficos candlestick.

O usuário pode fazer perguntas como:

“Qual a cotação do ouro no último mês?”

E receber uma resposta estruturada com:

dados históricos
métricas estatísticas
visualização gráfica
interpretação gerada por modelo de linguagem

📊 Visualização de dados com gráficos candlestick

O sistema transforma dados financeiros em visualizações interativas que facilitam a análise de tendência, volatilidade e variação de preços.

<img width="1303" height="443" alt="image" src="https://github.com/user-attachments/assets/8fa2cd9b-7432-4081-92ab-c7991dc645e5" />


⚙️ Como o sistema funciona

O chatbot interpreta a solicitação do usuário e executa automaticamente um fluxo de análise:

Identifica a commodity mencionada (ouro, petróleo, café etc.)
Coleta dados históricos via API do Yahoo Finance
Processa o período solicitado
Gera gráficos candlestick da variação de preços
Calcula métricas estatísticas:
média
mínimo e máximo
desvio padrão
variação percentual
Executa regras simples de análise (ex: condições baseadas em quartis)
Envia os dados estruturados para a API da OpenAI (GPT-3.5)
Retorna uma interpretação em linguagem natural

🧠 Ferramentas (Functions) da API

O sistema utiliza o recurso de function calling da OpenAI para integrar o modelo com dados reais.

Função	Descrição	Parâmetros
retorna_cotacao_commodity	Retorna a cotação atual de uma commodity	commodity, periodo
grafico_candlestick	Gera gráfico com estatísticas e análise de preço	commodity, periodo

🔧 Arquitetura do sistema

O fluxo principal está concentrado na função gera_texto, responsável por:

Gerenciar o histórico da conversa
Controlar chamadas à API da OpenAI
Executar funções locais quando solicitado pelo modelo
Retornar a resposta final ao usuário

🛠️ Tecnologias utilizadas
OpenAI API (GPT-3.5-turbo-0125)
yfinance (dados financeiros)
pandas (processamento de dados)
plotly (visualização de gráficos)
dotenv (configuração de ambiente)
regex e warnings (suporte auxiliar)

🏃‍♂️ Como executar

1. Configure a variável de ambiente:

OPENAI_API_KEY=...

2. Instale dependências:

pip install openai yfinance pandas plotly python-dotenv

3. Execute:

python ChatbotCommodities_PT.py

4. Exemplos de uso:

Qual a cotação do ouro no último mês?
Mostre o gráfico do petróleo nos últimos 3 meses.
Qual a cotação da prata hoje?

🧩 Estrutura do código
Dicionários de suporte para commodities e períodos
Funções de consulta e geração de gráficos
Integração com OpenAI via tools
Loop interativo via terminal

✨ Observações
Petróleo utiliza ticker CL=F (crude oil no Yahoo Finance)
Ajustes são feitos para commodities com precificação específica (ex: soja)
📽️ Demonstração

Vídeo mostrando o funcionamento do sistema:

➡️ https://www.loom.com/share/7cd45011502b427cbecf339aea972d93

📝 Licença

Projeto livre para adaptação e estudo.
