# Google Earth Engine Adapter Microservice

[![Build Status](https://travis-ci.org/resource-watch/adapter-earth-engine.svg?branch=dev)](https://travis-ci.org/resource-watch/adapter-earth-engine)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b221d818e0e99f94d0c8/test_coverage)](https://codeclimate.com/github/resource-watch/adapter-earth-engine/test_coverage)

This repository implements the Google Earth Engine Adapter services that are available in the Resource Watch API.

If you are looking for the API Doc (Info and Usage) please go to the next link:
[View the documentation for this
API] ()(NOT YET)

## Dependencies

Dependencies on other Microservices:
- [Geostore](https://github.com/gfw-api/gfw-geostore-api)
- [GFW OGR](https://github.com/gfw-api/gfw-ogr-api)

## Quick Overview

### Create a GEE Dataset

To create a new GEE dataset it's necessary to execute the following request.

Important:
- the connectorType value has to be "rest"
- the provider value has to be "gee"

```
POST: /dataset -> payload:
{
	"dataset": {
		"application": [<application-name>],
		"name": <dataset-name>,
		"connectorType": "rest",
		"provider": "gee",
		"tableName": <table-name>
	}
}
```

### Example (copy&paste)

```
POST: https://staging-api.globalforestwatch.org/dataset -> payload:
{
	"dataset": {
		"application": ["rw"],
		"name": "Data about whatever",
		"connectorType": "rest",
		"provider": "gee",
		"tableName": "ft:1qpKIcYQMBsXLA9RLWCaV9D0Hus2cMQHhI-ViKHo"
	}
}
```

Once the dataset has been saved (a few seconds after the creation) you can start doing queries to GEE.

### Fields

This endpoint returns the available fields in the dataset

```
GET: /fields/:dataset
```

Example (copy&paste)

```
GET: https://staging-api.globalforestwatch.org/fields/68353d61-0f47-4836-9699-72e008cd9f5f
```

### Query

This endpoint returns the execution of the SQL query (sql queryParam is required)

```
GET: /query/:dataset?sql=<slq_query>
```

Example (copy&paste)

```
GET: https://staging-api.globalforestwatch.org/query/68353d61-0f47-4836-9699-72e008cd9f5f?sql=select * from ft:1qpKIcYQMBsXLA9RLWCaV9D0Hus2cMQHhI-ViKHo where width > 100
```

### Download

Download the data in json format (csv coming soon)

```
GET: /download/:dataset?sql=<slq_query>
```

Example (copy&paste)

```
GET: https://staging-api.globalforestwatch.org/download/68353d61-0f47-4836-9699-72e008cd9f5f?sql=select * from ft:1qpKIcYQMBsXLA9RLWCaV9D0Hus2cMQHhI-ViKHo where width > 100
```


## Tests

As this microservice relies on Google Earth Engine, tests require a valid `storage.json` or equivalent file. 
At the time of this writing, actual tests use mock calls, so the real credential are only needed because Google's 
library actually validates the credentials on startup. 

Before you run the tests, be sure to install the necessary development libraries, using `pip install -r requirements_dev.txt`.

Actual test execution is done by running the `pytest` executable on the root of the project.  
