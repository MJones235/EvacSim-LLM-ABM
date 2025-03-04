from flask import Flask, request, jsonify
from src.services.run_service import RunService
from src.services.llm_service import LLMService
from src.services.population_service import PopulationService

app = Flask(__name__)
run_service = RunService()
llm_service = LLMService()
population_service = PopulationService(None)

@app.route("/runs", methods=["GET"])
def get_runs():
    runs = run_service.get_all_runs()
    return jsonify(runs)

@app.route("/population/<run_id>", methods=["GET"])
def get_population(run_id):
    population = population_service.get_population(run_id)
    return jsonify(population)

@app.route("/llm_logs/<run_id>", methods=["GET"])
def get_llm_logs(run_id):
    logs = llm_service.get_logs_by_run_id(run_id)
    return jsonify(logs)

@app.route("/agent_log/<agent_id>", methods=["GET"])
def get_agent_log(agent_id):
    # Placeholder for future enhancement
    return jsonify({"message": "Agent log retrieval not yet implemented"})

if __name__ == "__main__":
    app.run(debug=True)