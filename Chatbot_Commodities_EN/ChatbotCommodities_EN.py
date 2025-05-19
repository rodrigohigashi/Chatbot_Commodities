# Importing required libraries
import json
import yfinance as yf
import pandas as pd
import warnings
import re
import plotly.graph_objects as go 

import openai
from dotenv import load_dotenv, find_dotenv

# Environment setup, OpenAI client initialization, and warning suppression
warnings.filterwarnings("ignore", category=FutureWarning)  # suppress warnings

_ = load_dotenv(find_dotenv())

client = openai.Client()

# Support dictionaries: mapping of commodities and time periods

# Maps Portuguese commodity names to their Yahoo Finance ticker symbols
commodities_map = {
    'gold': 'GC=F',
    'silver': 'SI=F',
    'crude oil': 'CL=F',
    'corn': 'ZC=F',
    'wheat': 'ZW=F',
    'coffee': 'KC=F',
    'cocoa': 'CC=F',
    'soybean': 'ZS=F',
    'cotton': 'CT=F',
    'oat': 'ZO=F'
}

# Translation of natural language time periods to API-compatible format
period_translations = {
    "1 day": "1d",
    "1 week": "7d",
    "1 month": "1mo",
    "2 months": "2mo",
    "3 months": "3mo",
    "6 months": "6mo",
    "1 year": "1y"
}

# Inverted dictionary to allow for validation and user-friendly display
valid_periods = {v: k for k, v in period_translations.items()}

# Function that returns the most recent price of a commodity for the given period
def get_commodity_price(commodity, period):
    ticker = commodities_map.get(commodity.lower())  # Get the corresponding ticker

    if not ticker:
        return f"Commodity '{commodity}' not found. Try one of the following: {', '.join(commodities_map.keys())}."

    # Set default period and validate input
    period = period.lower() if period else '1mo'
    if period not in valid_periods:
        return f"Period '{period}' is not valid. Try one of the following: {', '.join(valid_periods.keys())}."

    # Fetch historical price data for the commodity
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(period=period)['Close']

    if hist.empty:
        return f"No data found for {commodity} in the period '{period}'."

    latest_price = hist[-1]

    # Adjust price for commodities quoted in cents (e.g., soybeans)
    if ticker == 'ZS=F':
        latest_price /= 100

    return f"The most recent price of {commodity} is ${latest_price:.2f}"

#######################################################################################

# Generates a candlestick chart with statistics and potential price alerts for a given commodity
def candlestick_chart(commodity, period='1mo'):
    ticker = commodities_map.get(commodity.lower())
    if not ticker:
        return f"Commodity '{commodity}' not found."

    try:
        hist = yf.Ticker(ticker).history(period=period)
        if hist.empty:
            return f"No data found for {commodity} in the period '{period}'."

        hist.index = pd.to_datetime(hist.index)

        # Check if essential columns are present and valid
        if any(col not in hist.columns or hist[col].isnull().all() for col in ['Open', 'High', 'Low', 'Close']):
            return f"Insufficient data to generate the chart for {commodity} ({period})."

        readable_period = valid_periods.get(period, period)

        # Base candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close']
        )])

        # Statistics
        avg_price = hist['Close'].mean()
        min_price = hist['Close'].min()
        max_price = hist['Close'].max()
        std_dev = hist['Close'].std()
        q1 = hist['Close'].quantile(0.25)
        start_price, end_price = hist['Close'].iloc[0], hist['Close'].iloc[-1]
        variation = ((end_price - start_price) / start_price) * 100

        annotation_text = (
            f"Average: {avg_price:.2f} | Min: {min_price:.2f} | Max: {max_price:.2f} | "
            f"Standard Deviation: {std_dev:.2f} | Change: {variation:.2f}%"
        )

        # Layout settings
        fig.update_layout(
            title=dict(
                text=f'{commodity.capitalize()} Candlestick Chart ({readable_period})',
                x=0.5, font=dict(size=22)
            ),
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            xaxis_rangeslider_visible=False,
            margin=dict(t=80, b=250, l=50, r=50),
            plot_bgcolor='white',
            autosize=True
        )

        # Add statistics annotation
        fig.add_annotation(
            text=annotation_text,
            xref="paper", yref="paper",
            x=0.5, y=-0.4,
            showarrow=False,
            font=dict(size=12)
        )

        # Alert if the latest price is below or equal to Q1
        alert_text = ""
        if end_price <= q1:
            alert_text = f"⚠️ Alert: the latest closing price is below or equal to the first quartile (Q1 = {q1:.2f})."
            fig.add_annotation(
                text=alert_text,
                xref="paper", yref="paper",
                x=0.5, y=-0.5,
                showarrow=False,
                font=dict(size=14, color="red")
            )

        fig.show(block=False)

        return f"{commodity.capitalize()} chart for {readable_period} displayed successfully.\n{annotation_text}{alert_text}"

    except Exception as e:
        if 'rate limit' in str(e).lower():
            return "Rate limit reached for the financial data API. Please try again later."
    import traceback
    traceback.print_exc()
    return f"Error generating chart: {type(e).__name__} - {e}"

##############################################################################################

# Tools (if there are specific tools used in the code)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_commodity_price",
            "description": "Returns the current price of a commodity such as gold, silver, oil, coffee, or corn.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commodity": {
                        "type": "string",
                        "description": "Name of the commodity (e.g., oil, gold, corn, coffee)"
                    },
                    "period": {
                        "type": "string",
                        "description": "Period to display data for, such as '1d', '5d', '1mo', '3mo', '6mo', '1y', or '5y'"
                    }
                },
                "required": ["commodity", "period"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "candlestick_chart",
            "description": "Generates a candlestick chart for a commodity over a specified period, with statistics and price alerts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commodity": {
                        "type": "string",
                        "description": "Name of the commodity (e.g., oil, gold, corn, coffee)"
                    },
                    "period": {
                        "type": "string",
                        "description": "Period to display data for, such as '1d', '5d', '1mo', '3mo', '6mo', '1y', or '5y'"
                    }
                },
                "required": ["commodity"]
            }
        }
    }
]

# Dictionary of functions the agent can call
available_functions = {
    "get_commodity_price": get_commodity_price,
    "candlestick_chart": candlestick_chart
}

#########################################################################

# Function that interacts with the OpenAI API and generates the chatbot response
def generate_text(messages, force_tool=False):
    if force_tool:
        tool_choice = {"type": "function", "function": {"name": "candlestick_chart"}}
    else:
        tool_choice = 'auto'

    response = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        messages=messages,
        tools=tools,
        tool_choice=tool_choice
    )

    primary_response = response.choices[0].message
    messages.append(primary_response)

    if primary_response.tool_calls:
        for call in primary_response.tool_calls:
            function_name = call.function.name
            arguments = json.loads(call.function.arguments)

            result = available_functions[function_name](**arguments)

            messages.append({
                'role': 'tool',
                'tool_call_id': call.id,
                'name': function_name,
                'content': result
            })

        final_response = client.chat.completions.create(
            model='gpt-3.5-turbo-0125',
            messages=messages
        )
        messages.append(final_response.choices[0].message)

    return messages

if __name__ == '__main__':
    print('Welcome to the Commodities ChatBot.')
    messages = []

    while True:
        user_input = input('User: ')
        messages.append({'role': 'user', 'content': user_input})

        # You can temporarily set force_tool=True here if you want to force the function execution
        messages = generate_text(messages, force_tool=False)

        # Check if the last message is from the assistant and print it
        if messages and messages[-1].role == 'assistant' and hasattr(messages[-1], 'content'):
            print(f"Assistant: {messages[-1].content}")