from src.CaseMemory import CaseMemory
from src.PromptManager import PromptManager
from src.LLMClient import LLMClient
from src.AutoRedTeamer import AutoRedTeamer

from src._configs import NodeConfigs


if __name__ == "__main__":
    client = LLMClient(model_name="mixtral", temperature=0.5)

    manager = PromptManager()
    memory = CaseMemory()

    auto_red_teamer = AutoRedTeamer(NodeConfigs)

    test_subject = "racism"
    max_test_iterations = 3

    auto_red_teamer.run_red_team_event(test_subject=test_subject,
                                       llm_client=client,
                                       llm_test=client,
                                       prompt_manager=manager,
                                       case_memory=memory,
                                       max_test_iterations=max_test_iterations)

