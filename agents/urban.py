from llm import get_llm_with_fallback
from langchain_core.output_parsers import JsonOutputParser

llm = get_llm_with_fallback()

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