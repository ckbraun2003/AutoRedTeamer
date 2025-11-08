from src._node import Node
from src._memory import CaseMemory
from src._manager import PromptManager
from src._llmclient import LLMClient
from src._utils import *

class NodeConfigs:
    configs = {
        "risk_analyzer":
            {"required_keys": None,
             "expected_type": str,
             "max_iterations": 3},

        "seed_prompt_generator":
            {"required_keys": ["testcaseidx", "description", "expected outcome", "input data"],
             "expected_type": list,
             "max_iterations": 3},

        "strategy_designer":
            {"required_keys": ["testcaseidx", "justification", "selected attack"],
             "expected_type": dict,
             "max_iterations": 3},

        "evaluator":
            {"required_keys": ["testcaseidx", "safety assessment", "strengths", "weaknesses", "safety score"],
             "expected_type": dict,
             "max_iterations": 3},

        "relevancy_checker":
            {"required_keys": ["testcaseidx", "relevance", "coverage", "needs replacement", "needs refinement"],
             "expected_type": dict,
             "max_iterations": 3},
    }

    @classmethod
    def items(cls):
        return cls.configs.items()


class AutoRedTeamer:

    def __init__(self,
                 prompt_manager: PromptManager,
                 llm_client: LLMClient,
                 case_memory: CaseMemory,
                 node_configs: NodeConfigs):

        self._manager = prompt_manager
        self._client = llm_client
        self._memory = case_memory

        self.nodes = self._get_nodes(node_configs)


    @staticmethod
    def _get_nodes(node_configs: NodeConfigs) -> dict[str, Node]:

        nodes = {}
        for name, cfg in node_configs.items():
            nodes[name] = Node(
                required_keys=cfg["required_keys"],
                expected_type=cfg["expected_type"],
                max_iterations=cfg["max_iterations"]
            )
        return nodes


if __name__ == "__main__":
    manager = PromptManager()
    client = LLMClient(model_name="mixtral", temperature=0.5)
    memory = CaseMemory()
