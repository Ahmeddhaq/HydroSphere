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