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

1. Geo location
2. Device ID
3. Metric ID
4. Parameter ID

Of course we did not pick up these labels at random from a crossword puzzle. They are chosen with meaning, as described in the following subsections:-

### Locations

Three types of locations are used for distributed deployment, to keep track of the deployment scheme, architecture and platform used. These are:-

- **Infrastructure Location** - What type of device or architecture used for the deployment. In case of Unified sensor Nework standards, these can be either WROOM32 or ARMv6/v7. Generally, all remote slave devices are hosted on ESP32, thus, we consider all our edge infrastucture to be uniformly, WROOM32.

- **Platform Location** - What platform is making use of the client device data or serving it. In case of USN, it is always, charcoalAPI

- **Geo Location** - Where is the device physically? This tag is subject to change and devices with similar configuration can be found on different locations. Thus a location tag, generally mapped to an actual ohysical address is mandatorily used in the metadata.

### Device

A certain geo location may involve many different devices. We must be sure which device is sending the data, thus, a device ID or NodeID is used.

### Metrics

What physical inference should we make from the data stored in the tables? Is it acceleration, environment monitoring, or pollution monitoring? The metric ID differentiates physical data types from one another, helping us to determinem which sensor (out of the numerous connected to the slave device) has read those values.

### Parameters

Many times, we do not get a solitary parameter with a metric. Acceleration is almost always measured on three axes; x, y and z. Pollution monitoring may involve sensors that detect, not just CO and CO2, but also NOx and other particles. Thus, it is important to segregate each parameter from a sensor into different tables. This is where the parameter ID comes, at the very end of the heirarchy of the key based search algorithm.

## The first DB

Now that we know about the labels, lets get to creating our first database. Create a directory ```DB``` in the repo clone directory and create a file ```TestDB.db```.

Access this newly creagted database using the command

```BASH
$ sqlite3 TestDB.db
```

You'll now be in the sqlite shell. The next set of commands is to enable the column mode and table headers.

```sqlite
.headers on
.mode column
```

Let us now create our first table, the metadata table.

```SQL
CREATE 	TABLE metadata(
	tableID TEXT NOT NULL,
	geoLoc TEXT NOT NULL,
	deviceID TEXT NOT NULL,
	metricID TEXT NOT NULL,
	parameterID TEXT NOT NULL DEFAULT "NA"
);
```

This must generate the metadata table as required for our operations. The next step is t mannually enter the tags for each time series table. To insert data, we use the following example command.

```SQL
INSERT INTO metadata VALUES("t1", "LocTag_1", "ESP_1", "metric_0", "x1");
```

Keep meaningfull tags as the entry into this table, as it is **for you**, the developer. Also, keep track of your location tags with an available dictionary.

Once the above step is done, it is wisest to create the table to store data. It is a one line command that remains the same for all tables here-on.

```SQL
CREATE TABLE t1(
	epoch BIGINT NOT NULL,
	metric FLOAT NOT NULL
);
```

> Do not forget the ";" after every command.

Once created, the charcoalAPI automatically handles the read and write of data with these tables.

To view the data stored, you can easily enter the following line.

```SQL
SELECT * FROM t1;
```

With  time, it may happen that the API becomes slow because the tables are being populated faster than they are cleared. In those cases, we need to truncate the tables, or delete the values.

```SQL
DELETE FROM t1;
```

SQL is case-insensitive, thus, you can write all the above commands in small. It may as well go unsaid, do not repeat a name in case change as you do in other programming languages. MeTaDaTa and metdata are same to sqlite.
