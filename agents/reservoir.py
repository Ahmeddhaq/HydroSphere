from llm import get_llm_with_fallback
from langchain_core.output_parsers import JsonOutputParser

llm = get_llm_with_fallback()


parser = JsonOutputParser()


def reservoir_agent(state):

    prompt = f"""
You are the Reservoir Intelligence Agent.

Analyze the reservoir data below.

Data:
{state["reservoir_data"]}

Evaluate:
- Current water availability
- Storage condition
- Inflow vs outflow
- Recommended water release strategy

Return JSON with:
status,
storage_level,
risk,
recommendation
"""

    response = llm.invoke(prompt)

    result = parser.parse(response.content)

    return {
        "reservoir_analysis": result
    }