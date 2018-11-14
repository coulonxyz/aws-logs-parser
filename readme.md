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
  "region": "eu-central-1",
  "log_group_name": "/aws/lambda/my_lambda",
  "log_age_limit_in_seconds": 7200,
  "number_of_log_streams_to_check": 10,
  "filter_string": "SessionLogs"
}

```

## usage

> cd my_directory/aws-logs-custom-parser
> python parser.py