import streamlit as st
from src.services.agent_decision_service import AgentDecisionService
from src.services.run_service import RunService
from src.services.llm_service import LLMService
from src.services.population_service import PopulationService

crs = "epsg:27700"

# Initialize services
run_service = RunService()
llm_service = LLMService()
population_service = PopulationService(crs)
agent_decision_service = AgentDecisionService()

# Streamlit UI
st.title("EvacSim Database Browser")

# Select Run
title = "Select a Run"
runs = run_service.list_runs()
run_options = {run[0]: f"{run[1]} - {run[3]} ({run[5]} agents) - {run[2]}" for run in runs}
selected_run_id = st.selectbox(title, options=list(run_options.keys()), format_func=lambda x: run_options[x])

if selected_run_id:
    st.subheader("Population")
    columns = ["id", "name", "age", "occupation", "current_location", "current_activity", "leave_time", "plans"]
    population = population_service.get_population(selected_run_id)
    population_df = [{k: v for k, v in item.items() if k in columns} for item in population]
    st.dataframe(population_df, hide_index=True)

    st.subheader("Agent Decision Log")
    agent_options = {agent["id"]: f"{agent['name']} ({agent['occupation']})" for agent in population_df}
    selected_agent_id = st.selectbox("Select an Agent", options=list(agent_options.keys()), format_func=lambda x: agent_options[x])

    if selected_agent_id:
        decisions = agent_decision_service.get_agent_decisions(selected_agent_id)
        if decisions:
            st.dataframe(
                decisions,
                column_order=("timestamp", "previous_location", "previous_activity", "next_location", "next_activity", "reason"),
            )
        else:
            st.write("No decisions recorded for this agent.")

    st.subheader("LLM Logs")
    logs = llm_service.get_logs_by_run_id(selected_run_id)
    st.dataframe(logs, column_order=("prompt", "response", "timestamp"))
    