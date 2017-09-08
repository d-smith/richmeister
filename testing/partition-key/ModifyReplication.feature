Feature: ModifyReplication
    To verify modify replication we run the following scenarios

    Scenario Outline: Modify Replication
        Given item <item>
        When I modify it
        And replication runs
        Then I expect <region>

    Examples:
        | item | region |
        | b1   | east   |
        | b2   | east   |
        | b3   | west   |
        | b4   | east   |
        | b5   | west   |
        | b6   | west   |