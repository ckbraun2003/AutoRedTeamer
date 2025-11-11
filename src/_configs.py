class NodeConfigs:
    configs = {
        "risk_analyzer":
            {"required_keys": None,
             "expected_type": str,
             "max_iterations": 5},

        "seed_prompt_generator":
            {"required_keys": ["testcaseidx", "description", "expected outcome", "input data"],
             "expected_type": list,
             "max_iterations": 5},

        "strategy_designer":
            {"required_keys": ["testcaseidx", "justification", "selected attack"],
             "expected_type": dict,
             "max_iterations": 5},

        "evaluator":
            {"required_keys": ["testcaseidx", "safety assessment", "strengths", "weaknesses", "safety score"],
             "expected_type": dict,
             "max_iterations": 5},

        "relevancy_checker":
            {"required_keys": ["testcaseidx", "relevance", "coverage", "needs replacement", "needs refinement"],
             "expected_type": dict,
             "max_iterations": 5},
    }

    @classmethod
    def items(cls):
        return cls.configs.items()