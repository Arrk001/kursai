import os
from openai import OpenAI
from dotenv import load_dotenv
from rich import print
import json
# Import both definitions and both functions
from tools import get_weather_definition, get_weather, forecast_definition, forecast 

load_dotenv()

# GEN AI Params
API_KEY = os.getenv("GH_API_TOKEN")
PLATFORM_ENDPOINT = "https://models.github.ai/inference"
MODEL = "openai/gpt-4.1-mini"
# Other Params
EXIT_KEYWORDS = ["exit", "end", "finish", "bye", "stop", "byebye"]


client = OpenAI(base_url=PLATFORM_ENDPOINT, api_key=API_KEY)

messages = [{"role": "system", "content": "You are a helpful assistant. You answer only questions about the weather. You should not expand too much, just focus on the information you get from tools"}]


while True:
    prompt = input("User: ").strip()

    if prompt.lower() in EXIT_KEYWORDS:
        break

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        # Pass both tool definitions
        tools=[get_weather_definition, forecast_definition], 
        tool_choice="auto"
    )
    
    tool_calls = response.choices[0].message.tool_calls

    if tool_calls: # Check if tool_calls is not None or empty
        tool_call = tool_calls[0] # Assuming only one tool call for simplicity

        # Dispatch based on the tool name
        if tool_call.function.name == "weather":
            try:
                city = json.loads(tool_call.function.arguments)["city"]
                tool_response = get_weather(city)
            except json.JSONDecodeError:
                tool_response = {"error": "Could not parse arguments for weather tool."}
            except KeyError as e:
                tool_response = {"error": f"Missing argument for weather tool: {e}"}

        elif tool_call.function.name == "forecast":
            try:
                args = json.loads(tool_call.function.arguments)
                city = args["city"]
                days = args["days"]
                tool_response = forecast(city, days)
            except json.JSONDecodeError:
                tool_response = {"error": "Could not parse arguments for forecast tool."}
            except KeyError as e:
                tool_response = {"error": f"Missing argument for forecast tool: {e}"}
            except Exception as e:
                tool_response = {"error": f"An unexpected error occurred while calling forecast: {e}"}
        else:
            tool_response = {"error": f"Unknown tool called: {tool_call.function.name}"}

        # Handle tool response (including errors from the tool function)
        if "error" in tool_response:
            chatbot_response = f"I'm sorry, I encountered an issue: {tool_response['error']}"
            print(f"[red]AI: [/red] {chatbot_response}")
            messages.append({"role": "assistant", "content": chatbot_response}) # Add to messages for context
            continue # Continue to the next user prompt
        
        tool_response_as_text = json.dumps(tool_response)

        messages.append({"role": "assistant", "tool_calls": [tool_call]})
        messages.append({"role": "tool", "tool_call_id": tool_call.id,
                                 "content": str(tool_response_as_text)})

        # Second API call to get the chatbot's final response
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=[get_weather_definition, forecast_definition], # Pass tools again
            tool_choice="auto"
        )
        chatbot_response = response.choices[0].message.content

    else:
        # If no tool was called, the initial response is the direct answer
        chatbot_response = response.choices[0].message.content

    print(f"[green]AI: [/green] {chatbot_response}")