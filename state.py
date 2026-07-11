from typing import TypedDict

class HydroState(TypedDict):

    weather_data: dict
    reservoir_data: dict
    agriculture_data: dict
    urban_data: dict

    weather_analysis: dict
    reservoir_analysis: dict
    agriculture_analysis: dict
    urban_analysis: dict

    risk_analysis: dict

    final_decision: dict