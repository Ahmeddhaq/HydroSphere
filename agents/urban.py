import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    base_url="https://api.puter.com/puterai/openai/v1/",
    api_key=os.getenv("PUTER_API_KEY"),
    model="gpt-5.4-nano",
)

parser = JsonOutputParser()


def urban_agent(state):

    prompt = f"""
You are the Urban Water Demand Agent.

Analyze city water requirements.

Data:
{state["urban_data"]}

Evaluate:
- Domestic water requirement
- Industrial demand
- Priority

Return JSON:
water_demand,
priority,
recommendation
"""

    response = llm.invoke(prompt)

    result = parser.parse(response.content)

    return {
        "urban_analysis": result
    }