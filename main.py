import logging
import time

from src.CaseMemory import CaseMemory
from src.PromptManager import PromptManager
from src.LLMClient import LLMClient
from src.AutoRedTeamer import AutoRedTeamer

from src._configs import NodeConfigs

# Configure Logging
logging.basicConfig(
    level=logging.INFO,                   # Minimum log level to capture
    format="%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),          # Logs to console
        logging.FileHandler("system.log")    # Logs to a file
    ]
)

logger = logging.getLogger("AutoRedTeamer")
client = LLMClient(model_name="mixtral", temperature=0.5)

if __name__ == "__main__":

    test_model_name = "mixtral"
    test_subject = "racism"
    num_testcases = 2
    max_test_iterations = 2

    test_model = LLMClient(model_name=test_model_name, temperature=0.5)

    manager = PromptManager()
    memory = CaseMemory()

    auto_red_teamer = AutoRedTeamer(NodeConfigs)

    try:
        start_time = time.time()
        finished = auto_red_teamer.run_red_team_event(test_subject=test_subject,
                                       llm_client=client,
                                       llm_test=test_model,
                                       prompt_manager=manager,
                                       case_memory=memory,
                                       logger=logger,
                                       num_testcases=num_testcases,
                                       max_test_iterations=max_test_iterations)

        end_time = time.time()
        total_time_taken = (end_time - start_time) / 60

        if finished:
            print(f"""
            === AutoRedTeamer Diagnostics ===
            Test Subject      : {test_subject}
            Model Tested      : {test_model._model_name}
            Total Vulnerabilities : {memory.total_compromised}
            Total Testcases       : {memory.current_testcase_attempt}
            Total LLM Calls       : {client.llm_calls}
            Total Time Taken      : {total_time_taken:.2f} minutes
            ================================
            """)

        else:
            logger.error(f"Error occured -- (finished={finished})")

    except RuntimeError as e:
        logger.error(f"Error occured -- {e}")

