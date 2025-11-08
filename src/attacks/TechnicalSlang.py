from src.attacks._attack import BaseAttack

class TechnicalSlang(BaseAttack):

    def run(self):
        pass

    def generate_test_case(self, prompt: str) -> str:
        return prompt