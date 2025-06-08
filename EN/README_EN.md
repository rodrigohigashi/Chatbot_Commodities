# 🤖 Commodities ChatBot with OpenAI API and Yahoo Finance 📈

## About the Project

This interactive chatbot allows you to query real-time commodity prices and visualize financial commodity charts by integrating the OpenAI API with Yahoo Finance via `yfinance`. The bot understands natural language commands (English and Portuguese) and responds with financial data and dynamic charts.

---

## 📚 Libraries Used

- `openai` — For interacting with the OpenAI GPT API
- `yfinance` — To fetch historical and current financial commodity data
- `pandas` — Data manipulation and processing
- `plotly` — Creating interactive candlestick charts
- `dotenv` — Managing environment variables for API keys
- `warnings` and `re` — Support for warnings and regular expressions

---

## ⚙️ How the Chatbot Works

The bot is configured to recognize price and chart queries for commodities like gold, silver, crude oil, corn, coffee, among others.

### Available Tools (Functions) 🚀

The OpenAI API *tools* system enables the chatbot to call specific functions to get data or generate charts:

| Function                | Description                                                                       | Parameters                                                    |
|-------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------|
| `get_commodity_price` | Returns the current price of a commodity.                                         | `commodity` (name, e.g., "gold"), `period` (e.g., "1mo", "1d") |
| `candlestick_chart`    | Generates a candlestick chart with stats and price alerts for a commodity.         | `commodity` (name, e.g., "corn"), `period` (e.g., "3mo", "1y")  |

These functions are registered in a dictionary and can be dynamically called by the agent during conversation with the user.

---

## 🔧 How the Bot Interacts with the OpenAI API

The main flow happens in the `gera_texto` function:

- Receives the conversation messages history.
- Decides whether to force the use of a function (e.g., generate chart).
- Sends the messages to the OpenAI API, including tools configuration.
- When the API responds with a function call, the bot runs the corresponding local function.
- The function's return is appended to the history and a new API call generates the final user-facing response.
- Displays the assistant's final response.

This flow ensures the chatbot combines GPT intelligence with real financial data and custom visuals, delivering precise and rich answers.

---

## 🏃‍♂️ How to Use Locally

1. Set your OpenAI API key as environment variable (e.g., in `.env` file: `OPENAI_API_KEY=...`).
2. Install dependencies:
pip install openai yfinance pandas plotly python-dotenv

3. Run the main script:
python ChatbotCommodities_EN.py

4. Ask questions like:
- "What is the gold price in the last month?"
- "Show me the crude oil chart for the past 3 months."

---

## 🎯 Example Commands

- `What is the corn price for the last month?`
- `Show the coffee chart for the past 6 months.`
- `What is the silver price today?`

---

## 🛠️ Code Structure

- **Support dictionaries**: Map commodity names to Yahoo Finance tickers and translate natural language periods to API-accepted formats.
- **Query functions**: Fetch financial data and generate interactive charts.
- **OpenAI tool functions**: Exposed functions callable via the API.
- **Interactive loop**: Simple terminal interface for chatting with the bot.

---

## ✨ Notes

- Crude oil is referenced as "crude oil" and mapped to Yahoo Finance ticker `CL=F` to avoid confusion with generic oil.
- Specific adjustments are made for commodities priced in cents on Yahoo Finance (e.g., soybeans).

---

📽️ Video Demo

Watch a short walkthrough of the project: ➡️ [Click here to view on Loom](https://www.loom.com/share/0e6dd9371bf14e389564a0dec3183144)

---

## 📝 License

This project is open and adaptable as needed.

---

# Enjoy checking your favorite assets! 🚀📊
