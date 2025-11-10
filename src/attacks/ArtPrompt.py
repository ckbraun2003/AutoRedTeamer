from src.attacks.BaseAttack import BaseAttack

class ArtPrompt(BaseAttack):

    def generate_attack_prompt(self, prompt: str) -> str:
        return prompt