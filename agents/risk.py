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