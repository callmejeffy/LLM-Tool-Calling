import os, json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ticket_prices = {
    # ASIA (48)
    "afghanistan": "$780", "armenia": "$820", "azerbaijan": "$810", "bahrain": "$550", 
    "bangladesh": "$410", "bhutan": "$650", "brunei": "$180", "cambodia": "$220", 
    "china": "$290", "cyprus": "$880", "georgia": "$840", "india": "$350", 
    "indonesia": "$210", "iran": "$720", "iraq": "$850", "israel": "$920", 
    "japan": "$320", "jordan": "$740", "kazakhstan": "$680", "kuwait": "$590", 
    "kyrgyzstan": "$710", "laos": "$230", "lebanon": "$820", "malaysia": "$160", 
    "maldives": "$520", "mongolia": "$480", "myanmar": "$250", "nepal": "$430", 
    "north_korea": "$1200", "oman": "$580", "pakistan": "$490", "palestine": "$950", 
    "philippines": "$0", "qatar": "$610", "saudi_arabia": "$590", "singapore": "$190", 
    "south_korea": "$240", "sri_lanka": "$420", "syria": "$980", "taiwan": "$170", 
    "tajikistan": "$750", "thailand": "$200", "timor_leste": "$380", "turkey": "$780", 
    "turkmenistan": "$790", "uae": "$480", "uzbekistan": "$700", "vietnam": "$180", 
    "yemen": "$950",

    # EUROPE (44)
    "albania": "$920", "andorra": "$1050", "austria": "$880", "belarus": "$1100", 
    "belgium": "$870", "bosnia_herzegovina": "$940", "bulgaria": "$910", "croatia": "$930", 
    "czech_republic": "$890", "denmark": "$860", "estonia": "$950", "finland": "$920", 
    "france": "$910", "germany": "$860", "greece": "$890", "hungary": "$895", 
    "iceland": "$1200", "ireland": "$980", "italy": "$880", "latvia": "$960", 
    "liechtenstein": "$1100", "lithuania": "$960", "luxembourg": "$940", "malta": "$1050", 
    "moldova": "$980", "monaco": "$1200", "montenegro": "$970", "netherlands": "$870", 
    "north_macedonia": "$960", "norway": "$910", "poland": "$880", "portugal": "$990", 
    "romania": "$920", "russia": "$1050", "san_marino": "$1100", "serbia": "$940", 
    "slovakia": "$920", "slovenia": "$930", "spain": "$940", "sweden": "$890", 
    "switzerland": "$920", "ukraine": "$1050", "united_kingdom": "$899", "vatican_city": "$950",

    # AFRICA (54)
    "algeria": "$1150", "angola": "$1450", "benin": "$1550", "botswana": "$1350", 
    "burkina_faso": "$1600", "burundi": "$1580", "cabo_verde": "$1800", "cameroon": "$1520", 
    "central_african_republic": "$1700", "chad": "$1650", "comoros": "$1400", "congo_brazzaville": "$1550", 
    "dr_congo": "$1580", "djibouti": "$1250", "egypt": "$920", "equatorial_guinea": "$1680", 
    "eritrea": "$1350", "eswatini": "$1420", "ethiopia": "$1100", "gabon": "$1590", 
    "gambia": "$1750", "ghana": "$1480", "guinea": "$1720", "guinea_bissau": "$1780", 
    "ivory_coast": "$1550", "kenya": "$1050", "lesotho": "$1480", "liberia": "$1680", 
    "libya": "$1300", "madagascar": "$1350", "malawi": "$1450", "mali": "$1620", 
    "mauritania": "$1680", "mauritius": "$1200", "morocco": "$1100", "mozambique": "$1380", 
    "namibia": "$1320", "niger": "$1650", "nigeria": "$1350", "rwanda": "$1400", 
    "sao_tome_principe": "$1850", "senegal": "$1680", "seychelles": "$1150", "sierra_leone": "$1720", 
    "somalia": "$1400", "south_africa": "$1180", "south_suman": "$1550", "sudan": "$1380", 
    "tanzania": "$1150", "togo": "$1580", "tunisia": "$1080", "uganda": "$1320", 
    "zambia": "$1400", "zimbabwe": "$1380",

    # AMERICAS (35)
    "antigua_barbuda": "$1650", "argentina": "$1950", "bahamas": "$1450", "barbados": "$1600", 
    "belize": "$1550", "bolivia": "$1850", "brazil": "$1800", "canada": "$1050", 
    "chile": "$1900", "colombia": "$1750", "costa_rica": "$1580", "cuba": "$1620", 
    "dominica": "$1680", "dominican_republic": "$1550", "ecuador": "$1780", "el_salvador": "$1520", 
    "grenada": "$1700", "guatemala": "$1480", "guyana": "$1820", "haiti": "$1650", 
    "honduras": "$1540", "jamaica": "$1580", "mexico": "$1250", "nicaragua": "$1560", 
    "panama": "$1520", "paraguay": "$1880", "peru": "$1820", "st_kitts_nevis": "$1720", 
    "st_lucia": "$1710", "st_vincent_grenadines": "$1730", "suriname": "$1850", "trinidad_tobago": "$1780", 
    "usa": "$980", "uruguay": "$1920", "venezuela": "$1850",

    # OCEANIA (14)
    "australia": "$520", "fiji": "$850", "kiribati": "$1200", "marshall_islands": "$950", 
    "micronesia": "$880", "nauru": "$1100", "new_zealand": "$820", "palau": "$450", 
    "papua_new_guinea": "$480", "samoa": "$980", "solomon_islands": "$920", "tonga": "$1050", 
    "tuvalu": "$1300", "vanuatu": "$950"
}

def get_ticket_price(destination_city):
    price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
    return f"The price of a ticket to {destination_city} is {price}"

tools = [{
    "type": "function",
    "function": {
        "name": "get_ticket_price",
        "description": "Get the price of a return ticket.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination_city": {"type": "string"}
            },
            "required": ["destination_city"]
        }
    }
}]

def run_chat(user_input, history):
    # history is a list of messages passed from the backend
    messages = history + [{"role": "user", "content": user_input}]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )
    
    msg = response.choices[0].message
    
    if msg.tool_calls:
        messages.append(msg)
        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            result = get_ticket_price(args["destination_city"])
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
        
        # Second call to get the final natural language answer
        final_res = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return final_res.choices[0].message.content
    
    return msg.content