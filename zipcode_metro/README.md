A simple model and management code for mapping zipcodes to other useful things.

The management code fetches a zipped CSV file from our publically available 
S3 bucket, containing some public domain factual information about ZIP codes:

* City
* County
* "Primary statistical area", a.k.a. PSA, the "metro" of the ZIP code.
* State

This can be used for doing some rough but potentially useful bucketing
of campaign data (how much did such-and-such receive in funds originating
out-of-metro, etc).
