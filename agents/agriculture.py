from llm import get_llm_with_fallback
from langchain_core.output_parsers import JsonOutputParser

llm = get_llm_with_fallback()

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