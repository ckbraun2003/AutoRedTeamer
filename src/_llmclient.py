from typing import Optional

from langchain_community.llms import Ollama

class LLMClient:
    def __init__(self,
                 model_name: Optional[str] = None,
                 temperature: Optional[float] = 0.0):

        self.llm = Ollama(model=model_name, temperature=temperature) if model_name else Ollama(model="mixtral", temperature=temperature)

    def invoke(self,
               message: str) -> str:
        response = self.llm.invoke(message)
        return response