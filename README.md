# richmeister

[Makin' copies](http://www.nbc.com/saturday-night-live/video/copy-machine-ii/n10024?snl=1), specifically copies of records written to a DynamoDB table
in one region to another region.

This project implements a simple multi-master replication scheme for a DynamoDB
table that is present in two regions. The goal is to provide multi-master replication
for active-active two region application topologies.

This library imposes some requirements on the client:

* When creating or modifying an item in the replicated table, the caller must include three attributes:
    * ts - numeric timestamp, such as milliseconds since the epoch
    * wid - string write id attribute, used to break ties should conflicting writes with
    identical timestamps occur. A random uuid would work well.
    * replicate - a boolean attribute used to indicate if the item should be replicated. This attribute us stripped from the remote write, and we use its absence to eliminate replication cycles without having to traverse regions to use conflict resolution.

This solution consumes events from the DynamodDB table stream, and for the case where
replicate is true, writes the events to a FIFO queue, from which another lambda 
reads the record and replicates is subject to the conflict resolution criteria. The
use of the FIFO queue allows recovery of data from the source table for outages over
24 hours, and the conflict resolution strategy will honor writes made during the region
outage - the most recent user activity is preserved.

For conflict resolution, the latest timestamp will be the winner, and if timestamps are identical, the write ids are compared to select the write. 

The components can be installed using the provided cloud formation templates. Refer to the [jupyter](http://jupyter.org/) notebook in the testing directory to see what a multiregion set up looks like, and to view the test cases illustrating how conflict resolution works.