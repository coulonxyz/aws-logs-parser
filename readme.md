# aws logs parser

## installation

> cd my_directory

> git clone https://github.com/coulonxyz/aws-logs-parser.git

if you don't have boto3 installed globally on your computer: 
> sudo pip install boto3

(You can use sudo pip freeze to check.)

configure config.json (using config.json.sample as reference):
```
{
  "config_env_1": {
    "region": "eu-central-1",
    "log_group_name": "/aws/lambda/my-source-lambda",
    "log_age_limit_in_seconds": 7200,
    "number_of_log_streams_to_check": 10,
    "filter_string": "SessionLogs"
  },
  "config_env_2": {
    "region": "eu-central-1",
    "log_group_name": "/aws/lambda/my-dev-lambda",
    "log_age_limit_in_seconds": 1800,
    "number_of_log_streams_to_check": 10,
    "filter_string": "SessionLogs"
  },
  "config_env_3": {
    "region": "eu-central-1",
    "log_group_name": "/aws/lambda/my-prod-lambda",
    "log_age_limit_in_seconds": 60,
    "number_of_log_streams_to_check": 2,
    "filter_string": "SessionLogs"
  }
}
```

## usage

> cd my_directory/aws-logs-custom-parser

> python parser.py -c config_env_3 (where source is the name of the config environement)


## real life usage example

Tag some particular in your code, for instance:
> logger.warn('DEPRECATED: This method my_method is deprecated.')

build an config environment like this:

```
{
  {
  "deprecated_in_prod": {
    "region": "eu-central-1",
    "log_group_name": "/aws/lambda/my-prod-lambda",
    "log_age_limit_in_seconds": 7200,
    "number_of_log_streams_to_check": 10,
    "filter_string": "DEPRECATED"
  },
  ...
}
```

and run the command to retrieve quickly all the alarms raised with this filter:
> python parser.py -c deprecated_in_prod

et voilà.