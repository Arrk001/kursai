import streamlit as st
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from tools import get_weather_definition, get_weather, forecast_definition, forecast

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GH_API_TOKEN")
PLATFORM_ENDPOINT = "https://models.github.ai/inference"
MODEL = "openai/gpt-4.1-mini"

# Set up OpenAI client
client = OpenAI(base_url=PLATFORM_ENDPOINT, api_key=API_KEY)

# Set up Streamlit
st.set_page_config(page_title="Weather Chatbot", layout="centered")
st.title("☀️ Weather Chatbot")

# Initialize chat history and system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant. You answer only questions about the weather. You should not expand too much, just focus on the information you get from tools"}
    ]

# Show previous messages
for msg in st.session_state.messages[1:]:  # skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input from user
user_input = st.chat_input("Ask about the weather...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # First API call
    response = client.chat.completions.create(
        model=MODEL,
        messages=st.session_state.messages,
        tools=[get_weather_definition, forecast_definition],
        tool_choice="auto"
    )

    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:
        tool_call = tool_calls[0]

        # Dispatch to the appropriate tool
        try:
            args = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "weather":
                tool_response = get_weather(args["city"])
            elif tool_call.function.name == "forecast":
                tool_response = forecast(args["city"], args["days"])
            else:
                tool_response = {"error": f"Unknown tool: {tool_call.function.name}"}
        except Exception as e:
            tool_response = {"error": str(e)}

        # Handle tool response
        if "error" in tool_response:
            bot_reply = f"⚠️ Error: {tool_response['error']}"
        else:
            st.session_state.messages.append({
                "role": "assistant", "tool_calls": [tool_call]
            })
            st.session_state.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_response)
            })

            # Second API call
            second_response = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                tools=[get_weather_definition, forecast_definition],
                tool_choice="auto"
            )
            bot_reply = second_response.choices[0].message.content
    else:
        # No tool call; respond directly
        bot_reply = response.choices[0].message.content

    # Show and store bot reply
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
