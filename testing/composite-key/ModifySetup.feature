Feature: ModifySetup
    Before I run the modify feature I need some data set up in dynamo db

    Scenario Outline: Modify Setup
        Given east item <eid> <erk> <ets> <ewid>
        And west item <wid> <wrk> <wts> <wwid>
        Then I am ready to test

    Examples:
        | eid | erk | ets | ewid | wid | wrk | wts | wwid |
        | bb  | 1   | 100 | a    | bb  | 0   | 100 | a    |
        | bb  | 2   | 100 | a    | bb  | 2   | 90  | a    |
        | bb  | 3   | 100 | a    | bb  | 3   | 110 | a    |
        | bb  | 4   | 100 | z    | bb  | 4   | 100 | a    |
        | bb  | 5   | 100 | a    | bb  | 5   | 100 | z    |
        | bb  | 6   | 100 | a    | bb  | 6   | 100 | a    |