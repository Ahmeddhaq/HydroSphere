from langgraph.graph import StateGraph, END

from state import HydroState

from agents.weather import weather_agent
from agents.reservoir import reservoir_agent
from agents.agriculture import agriculture_agent
from agents.urban import urban_agent
from agents.risk import risk_agent
from agents.decision import decision_agent


# Create graph
workflow = StateGraph(HydroState)


# Add agents as nodes

workflow.add_node("weather", weather_agent)

workflow.add_node("reservoir", reservoir_agent)

workflow.add_node("agriculture", agriculture_agent)

workflow.add_node("urban", urban_agent)

workflow.add_node("risk", risk_agent)

workflow.add_node("decision", decision_agent)


workflow.set_entry_point("weather")


workflow.add_edge("weather", "reservoir")

workflow.add_edge("reservoir", "agriculture")

workflow.add_edge("agriculture", "urban")

workflow.add_edge("urban", "risk")

workflow.add_edge("risk", "decision")

workflow.add_edge("decision", END)


# Compile graph

hydro_graph = workflow.compile()