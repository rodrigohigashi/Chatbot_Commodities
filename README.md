# 🤖 ChatBot de Commodities com API da OpenAI e Yahoo Finance 📈

## Sobre o projeto

Este chatbot interativo permite consultar cotações e visualizar gráficos de commodities financeiras em tempo real, usando a integração entre a API da OpenAI e o Yahoo Finance via `yfinance`. O bot entende comandos em linguagem natural (Português e Inglês) e responde com informações financeiras e gráficos dinâmicos. 

---

## 📚 Bibliotecas usadas

- `openai` — Para interação com a API GPT da OpenAI
- `yfinance` — Para obter dados históricos e atuais de commodities financeiras
- `pandas` — Manipulação e tratamento dos dados
- `plotly` — Criação dos gráficos de candlestick interativos
- `dotenv` — Gerenciamento de variáveis de ambiente para chaves de API
- `warnings` e `re` — Suporte para tratamento de avisos e expressões regulares

---

## ⚙️ Como funciona o chatbot

O bot é configurado para reconhecer comandos de consulta de preços e gráficos para commodities como ouro, prata, petróleo (crude oil), milho, café, entre outras.

### Ferramentas (Functions) disponíveis 🚀

O sistema de *tools* da API OpenAI permite que o chatbot chame funções específicas para obter dados ou gerar gráficos:

| Função                 | Descrição                                                                            | Parâmetros                                                       |
|-----------------------|-------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| `retorna_cotacao_commodity` | Retorna a cotação atual de uma commodity.                                        | `commodity` (nome, ex: "ouro"), `periodo` (ex: "1mo", "1d")     |
| `grafico_candlestick`  | Gera um gráfico candlestick da commodity com estatísticas e alerta de preço.         | `commodity` (nome, ex: "milho"), `periodo` (ex: "3mo", "1y")    |

Essas funções estão registradas em um dicionário e podem ser chamadas dinamicamente pelo agente, conforme a conversa com o usuário.

---

## 🔧 Como o bot interage com a API OpenAI

O fluxo principal ocorre na função `gera_texto`:

- Recebe as mensagens já trocadas na conversa.
- Decide se deve forçar o uso de alguma função (ex: gerar gráfico).
- Envia as mensagens para a API da OpenAI, incluindo a configuração das *tools*.
- Quando a API responde com um chamado de função, o bot executa localmente a função correspondente.
- A resposta da função é então adicionada ao histórico e uma nova chamada à API é feita para gerar a resposta final ao usuário.
- Exibe a resposta final do assistente.

Esse fluxo garante que o chatbot combine a inteligência do GPT com dados financeiros reais e gráficos personalizados, entregando respostas precisas e visuais.

---

## 🏃‍♂️ Como usar localmente

1. Configure sua variável de ambiente com a chave da API da OpenAI (exemplo: `.env` com `OPENAI_API_KEY=...`).
2. Instale as dependências:
pip install openai yfinance pandas plotly python-dotenv

3. Execute o script principal:
python ChatbotCommodities_PT.py

4. Digite perguntas como:
- "Qual a cotação do ouro no último mês?"
- "Mostre o gráfico do petróleo nos últimos 3 meses."

---

## 🎯 Exemplos de comandos

- `Qual a cotação do milho no último mês?`
- `Mostre o gráfico do café nos últimos 6 meses.`
- `Qual a cotação da prata hoje?`

---

## 🛠️ Estrutura do código

- **Dicionários de suporte**: Mapeiam nomes de commodities para tickers Yahoo Finance e traduzem períodos de linguagem natural para formatos aceitos.
- **Funções de consulta**: Buscam dados financeiros e geram gráficos interativos.
- **Funções OpenAI tools**: São funções expostas para serem chamadas pela API.
- **Loop interativo**: Interface simples de terminal para conversar com o bot.

---

## 🎥 Demonstração em vídeo
Confira um vídeo demonstrando a interação com o chatbot, suas consultas e gráficos dinâmicos:

Assista ao vídeo no Loom: https://www.loom.com/share/7cd45011502b427cbecf339aea972d93

## ✨ Observações

- O petróleo está nomeado como "petróleo" em português e retornado com o ticker `CL=F` do Yahoo Finance, que representa o crude oil (petróleo bruto). Isso evita confusão entre óleo genérico e petróleo.
- Ajustes específicos são feitos para commodities cujo preço no Yahoo Finance está em centavos (ex: soja).

---

## 📝 Licença

Este projeto é aberto e pode ser adaptado conforme necessidade.

---

# Divirta-se consultando seus ativos favoritos! 🚀📊
