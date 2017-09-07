Feature: DeleteReplication
    To verify delete replication we run the following scenarios

    Scenario Outline: Delete Replication
        Given <thing> to delete
        When I delete it
        And delete replication runs
        Then result should be <this>

    Examples:
        | thing | this |
        | c1    | none   |
        | b1    | none   |
        | b3    | west   |
