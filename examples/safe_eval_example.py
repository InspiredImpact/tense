from tense.service_layer import safe_eval as time_exp_eval

CONSTANT = 3.14

# It works :)
exp = "2 + 2 * 2"
assert time_exp_eval.SafelyExpEvalute(exp).safe_evalute() == 6

# Flexible.
deps = {"minute": 60}
exp = "minute * 60"
assert time_exp_eval.SafelyExpEvalute(exp, eval_locals=deps).safe_evalute() == 3600

# Safety.
time_exp_eval.SafelyExpEvalute("globals().pop('CONSTANT')")
assert "CONSTANT" in globals()

time_exp_eval.SafelyExpEvalute("delattr(__builtins__, 'int')")
assert getattr(__builtins__, "int") is int
