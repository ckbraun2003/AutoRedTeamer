import json

from typing import Optional, Dict

class Evaluator:

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