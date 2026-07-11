from llm import get_llm_with_fallback
from langchain_core.output_parsers import JsonOutputParser

llm = get_llm_with_fallback()


parser = JsonOutputParser()


def decision_agent(state):

    prompt = f"""
You are the Decision & Allocation Agent.

Create the final water allocation strategy.

Consider:

Reservoir:
{state["reservoir_analysis"]}

Agriculture:
{state["agriculture_analysis"]}

Urban:
{state["urban_analysis"]}

Risk:
{state["risk_analysis"]}


Decide:
- agriculture allocation percentage
- urban allocation percentage
- reserve percentage
- explanation

Return JSON:
agriculture_allocation,
urban_allocation,
environmental_reserve,
reasoning
"""

    response = llm.invoke(prompt)

    result = parser.parse(response.content)

    return {
        "final_decision": result
    }