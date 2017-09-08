Feature: DeleteReplication
    To verify delete replication we run the following scenarios

    Scenario Outline: Delete Replication
        Given <thing> <sort> to delete
        When I delete it
        And delete replication runs
        Then result should be <this>

    Examples:
        | thing | sort | this   |
        | c1    | 0    | none   |
        | bb    | 1    | none   |
        | bb    | 3    | west   |
