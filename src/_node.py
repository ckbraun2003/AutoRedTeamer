import json

from typing import List, Dict, Optional

class Node:

    def __init__(self, required_keys: List[str] = None, max_iterations: int = 5, expected_type: type = dict) -> None:

        self._required_keys = required_keys
        self._max_iterations = max_iterations
        self._expected_type = expected_type

        self._cached_response = None

    def generate(self,
                 llm_client,
                 system_prompt: str):

        for _ in range(self.max_iterations):
            response = llm_client.invoke(system_prompt)

            try:
                parsed_response = json.loads(response)
            except json.JSONDecodeError:
                continue  # retry

            enforced_response = self._enforce_data_type(parsed_response, self.expected_type)
            if parsed_response is not None:
                self._cached_response = parsed_response
                return parsed_response

        raise RuntimeError("Failed to generate valid response after max iterations")

    def _enforce_data_type(self, response, expected_type: type):
        if expected_type is dict:
            if isinstance(response, expected_type):
                return self._check_required_keys(self.required_keys, response)

            if isinstance(response, list):
                if self._check_list_elements(response, expected_type):
                    self._enforce_data_type(response[0], expected_type)

        if expected_type is list and self.required_keys:
            return all(self._check_required_keys(self.required_keys, response) for item in response)

        if isinstance(response, expected_type):
            return response

        return None

    @staticmethod
    def _check_required_keys(required_keys: List[str], response: Dict[str, str]):
        if not required_keys:
            return response

        for key in required_keys:
            if key not in response:
                return None
        return response

    @staticmethod
    def _check_list_elements(response: list, expected_type: type):
        if all(isinstance(item, expected_type) for item in response):
            return response
        return None

    @property
    def previous_response(self) -> Optional[Dict[str, str], str]:
        return self._cached_response

    @property
    def max_iterations(self) -> int:
        return self._max_iterations

    @property
    def expected_type(self) -> type:
        return self._expected_type

    @property
    def required_keys(self) -> List[str]:
        return self._required_keys