# Google Earth Engine Adapter Microservice

This repository implements the Google Earth Engine Adapter services that are available in the Resource Watch API.

If you are looking for the API Doc (Info and Usage) please go to the next link:
[View the documentation for this
API] ()(NOT YET)

## Quick Overview

### Create a GEE Dataset

To create a new GEE dataset it's necessary to execute the following request.

Important:
- connectorType has to be "rest"
- provider has to be "gee"

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

### Example (real "copy&paste" example)

```
POST: http://staging-api.globalforestwatch.org/dataset -> payload:
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

When the dataset it's saved (a few seconds after the creation) you can start doing queries to GEE

### Fields

This endpoint returns the fields available in the dataset

```
GET: /fields/:dataset
```

Example (copy&paste)

```
GET: http://staging-api.globalforestwatch.org/fields/68353d61-0f47-4836-9699-72e008cd9f5f
```

### Query

This endpoint returns execution of the query (sql queryParam is required)

```
GET: /query/:dataset?sql=<slq_query>
```

Example (copy&paste)

```
GET: http://staging-api.globalforestwatch.org/query/68353d61-0f47-4836-9699-72e008cd9f5f?sql=select * from ft:1qpKIcYQMBsXLA9RLWCaV9D0Hus2cMQHhI-ViKHo where width > 100
```

### Download

Download the data in json format (csv coming soon)

```
GET: /download/:dataset?sql=<slq_query>
```

Example (copy&paste)

```
GET: http://staging-api.globalforestwatch.org/download/68353d61-0f47-4836-9699-72e008cd9f5f?sql=select * from ft:1qpKIcYQMBsXLA9RLWCaV9D0Hus2cMQHhI-ViKHo where width > 100
```
