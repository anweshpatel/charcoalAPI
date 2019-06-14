<!-- LICENSE NOTICE

charcoalAPI - IoT server-less API for Edge devices
Copyright (C) 2019 Anwesh Anjan Patel

This file is part of charcoalAPI.

charcoalAPI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

charcoalAPI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with charcoalAPI.  If not, see <https://www.gnu.org/licenses/>. -->

# Setting up the Database

This module takes you throught the short process of setting up the database for the charcoalAPI. These are subjected to change with the upcomming beta releases.


## Understanding Time series DB

Any time series database stores data in a "time series" table as shown below:-

epoch | vals
--- | ---
1558310401 | 22.1
1558310403 | 22.2
1558310405 | 22.5
... | ...
.. | ..
. | .

These tables, unlike relational databases, need to be annotated using metadata labels. These labels are stored in a special metadata table.

tableID | label1 | label2 | ... | ..
--- | --- | --- | --- | ---
t1 | tag1 | tag2 | ... | ..
t2 | tag4 | tag5 | ... | ..
... | ... | ... | ... | ..
.. | .. | .. | .. | .

By running a simple key-val search method, we can pin point the table where the related data is stored. It is then acessed to get the required data or to populate the table.

charcoalAPI is a built on an SQLite3 Relational DB and acts as a TSDB. As the edge devices on Unified Sensor Network are to be deployed on a "fire and forget" basis, the databse must be carefully, and manually prepared with the mandatory labels for the algorithm. In the subsequent sections, we shall see how to  set up the database with metadata table.

## Mandatory Labels

A few labels are set mandatory based on the first developmental and production environments where USN was deployed. These are :-

- Geo location
- Metric ID
- Parameter ID
- Device ID

These are not random labels
