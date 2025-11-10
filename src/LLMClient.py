from typing import Optional

from langchain_community.llms import Ollama

class LLMClient:
    def __init__(self,
                 model_name: Optional[str] = None,
                 temperature: Optional[float] = 0.0):

        self._llm = Ollama(model=model_name, temperature=temperature) if model_name else Ollama(model="mixtral", temperature=temperature)

        self._llm_calls = 0

    def invoke(self,
               message: str) -> str:
        response = self._llm.invoke(message)
        self._llm_calls += 1
        return response

    @property
    def llm_calls(self):
        return self._llm_calls