from abc import ABC, abstractmethod

class BaseNode(ABC):

    @abstractmethod
    def generate(self):
        '''This is the main function call for implementation'''
        pass

    @abstractmethod
    def format_prompt(self, **kwargs):
        '''Insert relevant inputs into system prompt here'''
        pass