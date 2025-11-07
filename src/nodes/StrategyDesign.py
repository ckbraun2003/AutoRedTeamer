import logging
import json
from typing import Optional, List, Dict

from src.nodes.BaseNode import BaseNode
from src._llmclient import LLMClient

class StrategyDesign(BaseNode):

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
                 all_attack_properties: List[str],
                 current_test_case: Dict[str, str],
                 combination_attack_success_rate: Optional[List[Dict[str, str]]] = None,
                 previous_attacks: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, str]]:

        self.logger.info(f"Generating strategy design dictionary for [{current_test_case["testcaseidx"]}]")

        message = self.format_prompt(all_attack_properties=all_attack_properties,
                                     current_test_case=current_test_case,
                                     combination_attack_success_rate=combination_attack_success_rate,
                                     previous_attacks=previous_attacks)
        response = self.llm_client.invoke(message=message)
        try:
            response_dict = json.loads(response)
            if type(response_dict) is list:
                response_dict = response_dict[0]

            if isinstance(response_dict, str):
                response_dict = json.loads(response_dict)
                # Check again if it's a list after the second parsing
                if type(response_dict) is list:
                    response_dict = response_dict[0]

            if "selected attack" not in response_dict.keys():
                return self.generate(all_attack_properties, current_test_case, combination_attack_success_rate,
                                     previous_attacks)

            if response_dict["selected attack"] not in all_attack_properties:
                return self.generate(all_attack_properties, current_test_case, combination_attack_success_rate, previous_attacks)

            return response_dict

        except json.decoder.JSONDecodeError:
            self.logger.debug(f"JSON Decode Error for [{current_test_case["testcaseidx"]}], re-iterating")
            self.logger.debug(response)
            return self.generate(all_attack_properties, current_test_case, combination_attack_success_rate, previous_attacks)


    def format_prompt(self,
                      all_attack_properties: List[str],
                      current_test_case: Dict[str, str],
                      combination_attack_success_rate: Optional[List[Dict[str, str]]] = None,
                      previous_attacks: Optional[List[Dict[str, str]]] = None) -> str:

        message = self.system_prompt.format(
            **{
            'all attack properties': all_attack_properties,
            'combination attack success rates': combination_attack_success_rate,
            'previous attacks': previous_attacks,
            'current test case': current_test_case
        })

        return message