Feature: Dot_tense service particle converters
  Rule: AbstractParticleConverter accepts only string value.
    Scenario Outline: GetattributeParticleConverter tests.
      Given we have <expression> and the potential <exp_type> of the value it will be converted to
      Then we assert that the result of converting a certain expression corresponds to a certain type

      Examples: Table of converted values.
        | expression          | exp_type    |
        | variable = 1        | T(int)      |
        | variable = 1, 2, 3  | T(list)     |
        | variable = true     | T(bool)     |
        | variable = false    | T(bool)     |
        | variable = exp(2*2) | T(int)      |
