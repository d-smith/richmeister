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
        Then I expect region to be <region>
    
    Examples:
        | id | ts  | wid | present | rts  | rwid  | repts | region |
        | a1 | 100 | a   | no      | 0    | x     | 100   | east   |
        | a2 | 100 | a   | yes     | 90   | x     | 100   | east   |
        | a3 | 100 | a   | yes     | 110  | x     | 110   | west   |
        | a4 | 200 | z   | yes     | 200  | a     | 200   | east   |
        | a5 | 300 | a   | yes     | 300  | z     | 300   | west   |
        | a6 | 400 | a   | yes     | 400  | a     | 400   | west   |