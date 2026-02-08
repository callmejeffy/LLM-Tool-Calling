from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)
MODEL = "gpt-4o-mini"

ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city):
    print(f"Tool called for city {destination_city}")
    price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
    return f"The price of a ticket to {destination_city} is {price}"

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}
tools = [{"type": "function", "function": price_function}]

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant that can provide flight ticket prices."
    }
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    messages.append({"role": "user", "content": user_input})

    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message

    # CASE 1: Model wants to call a tool
    if message.tool_calls:
        messages.append(message)

        for tool_call in message.tool_calls:
            if tool_call.function.name == "get_ticket_price":
                args = json.loads(tool_call.function.arguments)
                result = get_ticket_price(args["destination_city"])

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        # 🔹 Send tool result back to model
        final_response = openai.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        final_message = final_response.choices[0].message.content
        print(f"Chatbot: {final_message}")
        messages.append({"role": "assistant", "content": final_message})

    # CASE 2: Normal assistant reply
    else:
        print(f"Chatbot: {message.content}")
        messages.append({"role": "assistant", "content": message.content})