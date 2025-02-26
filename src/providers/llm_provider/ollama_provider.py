from src.providers.llm_provider.llm_provider import LLMProvider
import ray 
import json

class OllamaProvider(LLMProvider):
    def call_llm(self, prompt: str, format:str = "json"):
        
        @ray.remote
        def _ray_ollama_call(prompt, format):
            from langchain_ollama import OllamaLLM
            return OllamaLLM(model="llama3.2:3b", temperature=0.9, top_p=0.95, top_k=50, format=format).invoke(prompt)
        
        response = ray.get(_ray_ollama_call.remote(prompt, format))
        return json.loads(response) if format == "json" else response