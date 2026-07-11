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


def agriculture_agent(state):

    prompt = f"""
You are the Agriculture Demand Agent.

Analyze irrigation requirements.

Data:
{state["agriculture_data"]}

Evaluate:
- Crop water requirement
- Irrigation demand
- Priority level

Return JSON:
water_demand,
priority,
recommendation
"""

    response = llm.invoke(prompt)

    result = parser.parse(response.content)

    return {
        "agriculture_analysis": result
    }