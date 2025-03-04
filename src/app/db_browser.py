import streamlit as st
from src.services.run_service import RunService
from src.services.llm_service import LLMService
from src.services.population_service import PopulationService

crs = "epsg:27700"

# Initialize services
run_service = RunService()
llm_service = LLMService()
population_service = PopulationService(crs)

# Streamlit UI
st.title("EvacSim Database Browser")

# Select Run
title = "Select a Run"
runs = run_service.list_runs()
run_options = {run[0]: f"{run[2]} - {run[3]} ({run[5]} agents)" for run in runs}
selected_run_id = st.selectbox(title, options=list(run_options.keys()), format_func=lambda x: run_options[x])

if selected_run_id:
    st.subheader("Population")
    population = population_service.get_population(selected_run_id)
    st.dataframe(population)

    st.subheader("LLM Logs")
    logs = llm_service.get_logs_by_run_id(selected_run_id)
    st.dataframe(logs)
    
    # Future enhancement: Show individual agent logs
    # selected_agent = st.selectbox("Select an Agent", [agent["name"] for agent in population])
    # agent_log = get_agent_log(selected_agent)
    # st.write(agent_log)
