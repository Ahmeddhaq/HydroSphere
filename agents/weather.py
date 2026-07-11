from llm import get_llm_with_fallback

llm = get_llm_with_fallback()



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