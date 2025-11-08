from src.nodes import _node

class RiskAnalyzer(Node):

    def generate(self, user_input: str) -> str:

        categories = ["Summary", "Detailed Analysis", "Specific Test Case Scope"]
        message = self.format_prompt(user_input)
        response = self.llm_client.invoke(message=message)
        if all(category in response for category in categories):
            return response
        else:
            self.logger.debug(f"Missing analysis information for [{user_input}], re-iterating")
            self.logger.debug(response)
            return self.generate(user_input)

    @staticmethod
    def format_prompt(self,
                      user_input: str) -> str:

        message_parts = [self.system_prompt,
                         user_input]

        return "\n".join(message_parts)