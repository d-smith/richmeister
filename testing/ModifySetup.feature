Feature: ModifySetup
    Before I run the modify feature I need some data set up in dynamo db

    Scenario Outline: Modify Setup
        Given east item <eid> <ets> <ewid>
        And west item <wid> <wts> <wwid>
        Then I am ready to test

    Examples:
        | eid | ets | ewid | wid | wts | wwid |
        | b1  | 100 | a    | b0  | 100 | a    |
        | b2  | 100 | a    | b2  | 90  | a    |
        | b3  | 100 | a    | b3  | 110 | a    |
        | b4  | 100 | z    | b4  | 100 | a    |
        | b5  | 100 | a    | b5  | 100 | z    |
        | b6  | 100 | a    | b6  | 100 | a    |