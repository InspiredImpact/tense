from aiotense.service_layer import safe_eval as time_exp_eval

CONSTANT = 3.14


def time_exp_eval_demonstration() -> None:
    # It works :)
    exp = "2 + 2 * 2"
    assert time_exp_eval.SafelyExpEvalute(exp).safe_evalute() == 6

    # Flexible.
    deps = {"minute": 60}
    exp = "minute * 60"
    assert time_exp_eval.SafelyExpEvalute(exp, eval_locals=deps).safe_evalute() == 3600

    # Safely.
    time_exp_eval.SafelyExpEvalute("globals().pop('CONSTANT')")
    assert "CONSTANT" in globals()


if __name__ == "__main__":
    time_exp_eval_demonstration()
