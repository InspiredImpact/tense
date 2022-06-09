@fixture.config.emulation
@fixture.config.emulation.errors
Feature: Dot_tense service step_chain
  Scenario: First step tests.
    Given we have "config_emulation" value
    Then we create LexingStep object and .take_a_step() method should return instance of dict

  Scenario: Second step tests.
    Given we have instance of str "config_emulation" value for AnalyzeStep
    Then we create AnalyzeStep object and .take_a_step() method should return instance of dict

  Scenario: Second step raises test.
    Given we have "config_emulation_errors" value
    Then we can make sure that when parsing each of the configs, an error will be raised

  Scenario: Third step tests.
    Given we have instance of str "config_emulation" value for CompilingStep
    Then  we create CompilingStep object and .take_a_step() method should return instance of dict
    And the value of virtual units will change