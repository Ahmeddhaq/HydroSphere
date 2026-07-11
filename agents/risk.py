from llm import get_llm_with_fallback
from langchain_core.output_parsers import JsonOutputParser

llm = get_llm_with_fallback()


parser = JsonOutputParser()


def risk_agent(state):

    prompt = f"""
You are the Risk Assessment Agent.

Analyze the combined intelligence reports.

Weather:
{state["weather_analysis"]}

Reservoir:
{state["reservoir_analysis"]}

Agriculture:
{state["agriculture_analysis"]}

Urban:
{state["urban_analysis"]}


Determine:
- drought risk
- flood risk
- overall severity
- recommended action

Return JSON:
risk_type,
severity,
recommendation
"""

    response = llm.invoke(prompt)

    result = parser.parse(response.content)

    return {
        "risk_analysis": result
    }