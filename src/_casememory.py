import os
from typing import List


class CaseMemory:
    def __init__(self):

        self.initial_input = None
        self.risk_analysis = None

        self.test_cases = {}
        self.response_reports = {}
        self.evaluation_reports = {}
        self.relevancy_reports = {}

        self.short_term_memory = {}

    def get_attacks(self, path="attacks") -> List[str]:

        attack_types = [
            os.path.splitext(f)[0]  # removes the .py extension
            for f in os.listdir(path)
            if f.endswith('.py') and os.path.isfile(os.path.join(path, f))
        ]
        return attack_types

