from src.AutoRedTeamer import AutoRedTeamer
from src._systemprompts import system_prompts
from src._llmclient import LLMClient


if __name__ == "__main__":
    llm_client = LLMClient(model_name="mixtral", temperature=0.5)
    llm_tester = LLMClient(model_name="mixtral", temperature=0.5)

    model = AutoRedTeamer(llm_client=llm_client,
                          system_prompts=system_prompts,
                          llm_test=llm_tester)

    user_input = "racism"
    num_test_cases = 2
    max_iterations = 2
    save_to_file = True

    model.run_tests(user_input=user_input,
                    num_test_cases=num_test_cases,
                    max_iterations=max_iterations,
                    save_to_file=save_to_file)