FBPOOL Script
============= 

The purpose of the script fbpool.py is for database management.
The main purpose of this script is to load historical pool data into the database.

It can be used to:
* load data into the database
* manipulate the memcache
* query data in the database

## Step 1.  Specify the database URL and port number

When running the fbpool.py script, the database URL and port number need to be specified.
Specify the options in one of the following ways:

```
    python -p 10090 <.. more options>
    python --port 10090 <.. more options>
```

This will use the url http://localhost:10090 as the base URL.
The default URL is http://localhost.

```
    python -u http://cdcpool.appspot.com <.. more options>
    python --url http://cdcpool.appspot.com <.. more options>
```

This will use the url http://cdcpool.appspot.com as the base URL with no port number.
This is intended for loading the production database.

## Step 2.  How to load historical pool data into the database

The following commands can be used to load historical data into the database.

```
    python -p 10090 --load year -y 2013  
    python --port 10090 --load year --year 2013  
```

This will load all of the data for the year 2013.
The key argument here is "--load year" which indicates a year should be loaded.

Note that if no teams have been loaded yet, then the teams for year 2013 will be loaded. 
If teams in a prior year have been loaded (say 2012), then the team names and conferences
in the 2013 sheet will not overwrite the values from 2012.  

```
    python -p 10090 --load week -y 2013 -w 1
    python --port 10090 --load week --year 2013 --week 1
```

This will load all of the data for 2013 week 1.
The key argument here is "--load week" which indicates a week should be loaded.

