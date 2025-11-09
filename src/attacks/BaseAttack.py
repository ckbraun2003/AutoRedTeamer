from abc import abstractmethod

class BaseAttack:

    @abstractmethod
    def run(self):
        '''This is the main function call for implementation'''
        pass

    @abstractmethod
    def generate_test_case(self, prompt):
        '''Insert relevant inputs here, This function is for singular test case generation'''
        return prompt