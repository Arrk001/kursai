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

# Set up Streamlit page configuration (should be at the top)
st.set_page_config(page_title="Weatherbot", layout="centered")

# --- CUSTOM CSS FOR CENTERING TITLE AND BORDERS ---
st.markdown("""
<style>
/* Centering the H1 title */
h1 {
    text-align: center;
    width: 100%;
}

/* Base style for individual chat messages (apply common properties) */
.stChatMessage {
    border-radius: 5px; /* Slightly rounded corners */
    padding: 10px; /* Padding inside the border */
    margin-bottom: 10px; /* Space between message boxes */
    border-width: 1px; /* Ensure border width is set */
    border-style: solid; /* Ensure border style is set */
}

/* Lime green border for odd messages (1st, 3rd, 5th, etc.) */
/* Target the stChatMessage within the odd stLayoutWrapper */
div[data-testid="stLayoutWrapper"]:nth-child(odd) .stChatMessage {
    border-color: limegreen;
}

/* Light cyan border for even messages (2nd, 4th, 6th, etc.) */
/* Target the stChatMessage within the even stLayoutWrapper */
div[data-testid="stLayoutWrapper"]:nth-child(even) .stChatMessage {
    border-color: red;
}


/* Single border around the entire main content area (where all messages are) */
div[data-testid="stMainBlockContainer"] {
    border: 5px solid yellow !important; /* Main content border */
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
    margin-bottom: 20px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)
# --- END CUSTOM CSS ---

# Now display the title
st.title("☀️ Weatherbot 🌧️")


# Initialize chat history and system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant. You answer only questions about the weather. You should not expand too much, just focus on the information you get from tools"}
    ]

# Show previous messages
for msg in st.session_state.messages:
    # Skip system prompt and tool messages from being displayed in the chat window
    if msg["role"] == "system" or msg["role"] == "tool":
        continue

    # Determine the name based on the role
    if msg["role"] == "user":
        display_name = "You"
    elif msg["role"] == "assistant":
        display_name = "Weatherbot"
    else:
        display_name = None # For other roles, don't display a specific name

    # Only display messages that have a 'content' key (user and final assistant replies)
    if "content" in msg:
        with st.chat_message(msg["role"]):
            st.markdown(f"**{display_name}:** {msg['content']}")

# Input from user
user_input = st.chat_input("Ask about the weather...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f"**You:** {user_input}")

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
                # Current weather in Vilnius
                if args["city"].lower() == "vilnius":
                    tool_response = get_weather(args["city"])
                    tool_response["current_time"] = "Wednesday, June 25, 2025 at 2:20:01 PM EEST" # Updated current time
                else:
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
            # If there's an error, append it as an assistant message directly
            with st.chat_message("assistant"):
                st.markdown(f"**Weatherbot:** {bot_reply}")
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        else:
            # Append the assistant's tool call message (no content for display)
            st.session_state.messages.append({
                "role": "assistant", "tool_calls": [tool_call]
            })
            # Append the tool's response message (content for LLM, not for display)
            st.session_state.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_response)
            })

            # Second API call to get the human-readable response
            second_response = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                tools=[get_weather_definition, forecast_definition],
                tool_choice="auto"
            )
            bot_reply = second_response.choices[0].message.content
            # Show and store the final bot reply from the second API call
            with st.chat_message("assistant"):
                st.markdown(f"**Weatherbot:** {bot_reply}")
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    else:
        # No tool call; respond directly
        bot_reply = response.choices[0].message.content
        # Show and store bot reply
        with st.chat_message("assistant"):
            st.markdown(f"**Weatherbot:** {bot_reply}")
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})