from abc import ABC, abstractmethod

class BaseAttack(ABC):

    @abstractmethod
    def run(self):
        '''This is the main function call for implementation'''
        pass

    @abstractmethod
    def generate_test_case(self, **kwargs):
        '''Insert relevant inputs here, This function is for singular test case generation'''
        pass