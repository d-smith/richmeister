# richmeister

Makin' copies, specifically copies of records written to a DynamoDB instance
to other instances...

This project implements a simple multi-master replication scheme for a DynamoDB
table that is present in two regions. The goal is to initially support active-standby architectures with automated failover and failback, as well as to support active-active
configurations at some point as well.

This library imposes some requirements on the client:

* When creating or modifying an item in the replicated table, the caller must include three attributes:
    * ts - numeric timestamp, such as milliseconds since the epoch
    * wid - string write id attribute, used to break ties should conflicting writes with
    identical timestamps occur. A random uuid would work well.
    * replicate - a boolean attribute used to indicate if the item should be replicated. This attribute us stripped from the remote write, and we use its absence to eliminate replication cycles without having to traverse regions to use conflict resolution.

For conflict resolution, the latest timestamp will be the winner, and if timestamps are identical, the write ids are compared to select the write. 
