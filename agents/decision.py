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