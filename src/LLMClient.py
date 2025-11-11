from typing import Optional

from langchain_community.llms import Ollama

class LLMClient:
    def __init__(self,
                 logger = None,
                 model_name: Optional[str] = "mixtral",
                 temperature: Optional[float] = 0.0):

        self._logger = logger

        self._model_name = model_name
        self._llm = Ollama(model=model_name, temperature=temperature)

        self._llm_calls = 0

    def invoke(self,
               message: str) -> str:

        response = self._llm.invoke(message)
        self._llm_calls += 1
        if self._logger:
            self._logger.info(f"ModelName[{self._model_name}] -- [PROMPT]: {message}\n[RESPONSE]: {response}")
        return response

    @property
    def llm_calls(self):
        return self._llm_calls