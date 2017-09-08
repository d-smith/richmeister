Feature: ModifyReplication
    To verify modify replication we run the following scenarios

    Scenario Outline: Modify Replication
        Given id and sort <item> <sort>
        When I modify it
        And replication runs
        Then I expect <region>

    Examples:
        | item | sort | region |
        | bb   | 1    | east   |
        | bb   | 2    | east   |
        | bb   | 3    | west   |
        | bb   | 4    | east   |
        | bb   | 5    | west   |
        | bb   | 6    | west   |