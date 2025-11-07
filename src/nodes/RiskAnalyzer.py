import logging
from typing import Optional

from src.nodes.BaseNode import BaseNode
from src._llmclient import LLMClient

class RiskAnalyzer(BaseNode):

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

        self.llm_client = llm_client if not None else LLMClient("mixtral")
        self.system_prompt = system_prompt

        self.logger = logging.getLogger(self.__class__.__name__)

    def generate(self,
                 user_input: str) -> str:

        self.logger.info(f"Generating risk analysis for [{user_input}]")

        categories = ["Summary", "Detailed Analysis", "Specific Test Case Scope"]
        message = self.format_prompt(user_input)
        response = self.llm_client.invoke(message=message)
        if all(category in response for category in categories):
            return response
        else:
            self.logger.debug(f"Missing analysis information for [{user_input}], re-iterating")
            self.logger.debug(response)
            return self.generate(user_input)

    def format_prompt(self,
                      user_input: str) -> str:

        message_parts = [self.system_prompt,
                         user_input]

        return "\n".join(message_parts)