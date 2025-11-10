from src.attacks.BaseAttack import BaseAttack

class TechnicalSlang(BaseAttack):

    def generate_attack_prompt(self, prompt: str) -> str:
        return prompt