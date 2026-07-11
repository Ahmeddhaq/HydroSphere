import json

from graph import hydro_graph


# Load mock data
with open("data/mock_data.json", "r") as file:
    data = json.load(file)


# Initial shared state
initial_state = {

    "weather_data": data["weather"],

    "reservoir_data": data["reservoir"],

    "agriculture_data": data["agriculture"],

    "urban_data": data["urban"],


    # Empty fields
    "weather_analysis": {},

    "reservoir_analysis": {},

    "agriculture_analysis": {},

    "urban_analysis": {},

    "risk_analysis": {},

    "final_decision": {}
}


# Run the agent workflow
result = hydro_graph.invoke(initial_state)


print("\nFINAL WATER ALLOCATION DECISION")
print("--------------------------------")

print(result["final_decision"])