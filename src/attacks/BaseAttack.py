from abc import abstractmethod

class BaseAttack:

    @abstractmethod
    def generate_attack_prompt(self, prompt):
        '''Insert relevant inputs here, This function is for singular test case generation'''
        return prompt