from src.attacks.BaseAttack import BaseAttack

class Pliny(BaseAttack):

    def generate_attack_prompt(self, prompt: str) -> str:
        return prompt