Feature: InputReplication
    To verify insert replication works as expected
    we run replication with the following scenario outline

    Scenario Outline: Insert Replication
        Given an item with id <id>
        And range key <rk>
        And timestamp <ts>
        And wid <wid>
        And remote item <present>
        And remote rk <rrk>
        And remote ts <rts>
        And remote wid <rwid>
        When I replicate the insert
        Then I expect the remote ts <repts> 
        Then I expect region to be <region>
    
    Examples:
        | id | ts  | rk | wid | present | rrk | rts  | rwid  | repts | region |
        | a0 | 100 | 1  | a   | no      | 1   | 0    | x     | 100   | east   |
        | a1 | 100 | 1  | a   | yes     | 2   | 100  | a     | 100   | east   |
        | aa | 100 | 1  | a   | yes     | 1   | 90   | x     | 100   | east   |
        | aa | 100 | 2  | a   | yes     | 2   | 110  | x     | 110   | west   |
        | aa | 200 | 3  | z   | yes     | 3   | 200  | a     | 200   | east   |
        | aa | 300 | 4  | a   | yes     | 4   | 300  | z     | 300   | west   |
        | aa | 400 | 5  | a   | yes     | 5   | 400  | a     | 400   | west   |
 