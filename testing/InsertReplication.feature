Feature: InputReplication
    To verify insert replication works as expected
    we run replication with the following scenario outline

    Scenario Outline: Insert Replication
        Given an item with id <id>
        And timestamp <ts>
        And wid <wid>
        And remote item <present>
        And remote ts <rts>
        And remote wid <rwid>
        When I replicate the insert
        Then I expect the remote ts <repts> 
    
    Examples:
        | id | ts  | wid | present | rts  | rwid  | repts |
        | x1 | 100 | a   | no      | 0    | x     | 100   |