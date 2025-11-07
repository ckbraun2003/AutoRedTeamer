import logging
import json
from typing import Optional, Dict, List

from src.nodes.BaseNode import BaseNode
from src._llmclient import LLMClient

class SeedPromptGenerator(BaseNode):

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
                 num_test_cases: int,
                 subject: str,
                 test_requirements: str) -> List[Dict[str, str]]:

        self.logger.info(f"Generating [{num_test_cases}] test cases for [{subject}]")

        message = self.format_prompt(num_test_cases=num_test_cases,
                                     subject=subject,
                                     test_requirements=test_requirements)
        response = self.llm_client.invoke(message=message)
        try:
            response_dict = json.loads(response)
            return response_dict[:num_test_cases]

        except json.decoder.JSONDecodeError:
            self.logger.debug(f"JSON Decode Error for [{subject}], re-iterating")
            self.logger.debug(response)
            return self.generate(num_test_cases, subject, test_requirements)

    def refine_replace(self,
                       test_case: Dict[str, str],
                       subject: str) -> Dict[str, str]:

        return test_case


    def format_prompt(self,
                      num_test_cases: int,
                      subject: str,
                      test_requirements: str) -> str:

        message = self.system_prompt.format(
            **{
            'num test cases': num_test_cases,
            'subject': subject,
            'test requirements': test_requirements
        })

        return message