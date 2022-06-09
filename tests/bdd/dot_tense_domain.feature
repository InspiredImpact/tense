Feature: Dot_tense service domain
  Rule: HashableParticle accepts only string value.
    Scenario Outline: HeaderParticle tests.
      Given we have target <target> for HeaderParticle
      And we create HeaderParticle object
      Then we call .matches() method of HeaderParticle and it result will be equal to <matches>

      Examples: Table of matches.
        | target     | matches |
        | [header]   |  True   |
        | other      |  False  |
        | [ header ] |  True   |
        | [header    |  False  |
        | header]    |  False  |

    Scenario Outline: GetattributeParticle tests.
      Given we have target <target> for GetattributeParticle
      And we create GetattributeParticle object
      Then we call .matches() method of GetattributeParticle and it result will be equal to <matches>

      Examples: Table of matches.
        | target          | matches |
        | variable = 1 |  True   |
        | 1, 2, 3      |  False  |
        | [header]     |  False  |
        | variable=2   |  True   |
        | variable =2  |  True   |
        | variable= 2  |  True   |
