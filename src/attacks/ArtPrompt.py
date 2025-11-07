from src.attacks.BaseAttack import BaseAttack

class ArtPrompt(BaseAttack):

    def run(self):
        pass

    def generate_test_case(self, prompt: str) -> str:
        return prompt