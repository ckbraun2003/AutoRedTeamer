from typing import Optional

from langchain_community.llms import Ollama

class LLMClient:
    def __init__(self,
                 model_name: Optional[str] = "mixtral",
                 temperature: Optional[float] = 0.0):

        self._model_name = model_name
        self._llm = Ollama(model=model_name, temperature=temperature)

        self._llm_calls = 0

    def invoke(self,
               message: str) -> str:
        response = self._llm.invoke(message)
        self._llm_calls += 1
        return response

    @property
    def llm_calls(self):
        return self._llm_calls