# EvacSim-LLM-ABM

## Create virtual environment (optional)
```
python3 -m venv .venv
```

## Activate virtual environment (optional)
Linux
```
source .venv/bin/activate
```
Windows
```
.venv\Scripts\activate.bat
```

## Install dependencies
```
python3 -m pip install -r requirements.txt
```

## Pull LLM
Download [Ollama](https://ollama.com/download)
```
ollama run llama3.2:3b
```

## Set python path
```
set -a
source .env
```

## Run
```
solara run scripts/run.py
```
