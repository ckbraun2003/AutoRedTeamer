import logging
import json
from typing import Optional, List, Dict

from src.nodes.BaseNode import BaseNode
from src._llmclient import LLMClient

class RelevancyChecker(BaseNode):

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
                 user_input: str,
                 test_case: Dict[str, str],
                 test_prompt: str) -> List[Dict[str, str]]:

        self.logger.info(f"Generating relevancy dictionary for [{test_case["testcaseidx"]}]")

        message = self.format_prompt(user_input=user_input,
                                     test_case=test_case,
                                     test_prompt=test_prompt
                                     )
        response = self.llm_client.invoke(message=message)
        try:
            response_dict = json.loads(response)
            if type(response_dict) is list:
                return response_dict[0]
            else:
                return response_dict

        except json.decoder.JSONDecodeError:
            self.logger.debug(f"JSON Decode Error for [{test_case["testcaseidx"]}], re-iterating")
            self.logger.debug(response)
            return self.generate(user_input, test_case, test_prompt)


    def format_prompt(self,
                      user_input: str,
                      test_case: Dict[str, str],
                      test_prompt: str) -> str:

        message = self.system_prompt.format(
            **{
            'original input': user_input,
            'original scope': test_case,
            'test prompt': test_prompt
        })

        return message