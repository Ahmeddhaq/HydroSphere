import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    base_url="https://api.puter.com/puterai/openai/v1/",
    api_key=os.getenv("PUTER_API_KEY"),
    model="gpt-5.4-nano",
)


def weather_agent(state):

    prompt = f"""
You are the Weather Intelligence Agent
for a water management system.

Analyze this weather data:
from dotenv import load_dotenv

load_dotenv()
{state["weather_data"]}

Determine:
- rainfall condition
- evaporation risk
- water availability impact
- recommendation

Return JSON only.
"""

    response = llm.invoke(prompt)

    return {
        "weather_analysis": response.content
    }