import logging
import json
from typing import Optional, Dict

from src.nodes.BaseNode import BaseNode
from src._llmclient import LLMClient

class Evaluator(BaseNode):

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
        handlers=[
            logging.FileHandler('functions_log.txt'),
            logging.StreamHandler()  # Also log to console
        ]
    )

    def __init__(self,
                 llm_client: Optional[LLMClient] = None,
                 system_prompt: Optional[str] = None):

        self.llm_client = llm_client if not None else LLMClient()
        self.system_prompt = system_prompt

        self.logger = logging.getLogger(self.__class__.__name__)

    def generate(self,
                 test_case: str,
                 model_response: str) -> Dict[str, str]:

        self.logger.info(f"Generating evaluation dictionary for [{test_case["testcaseidx"]}]")

        message = self.format_prompt(test_case=test_case,
                                     model_response=model_response)
        response = self.llm_client.invoke(message=message)
        try:
            response_dict = json.loads(response)
            if type(response_dict) is list:
                response_dict = response_dict[0]

            if "safety score" not in response_dict.keys():
                return self.generate(test_case, model_response)

            return response_dict

        except json.decoder.JSONDecodeError:
            self.logger.debug(f"JSON Decode Error for [{test_case["testcaseidx"]}], re-iterating")
            self.logger.debug(response)
            return self.generate(test_case, model_response)


    def format_prompt(self,
                      test_case: str,
                      model_response: str) -> str:

        message = self.system_prompt.format(
            **{
            'test case': test_case,
            'model response': model_response
        })

        return message