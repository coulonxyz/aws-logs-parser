# !/usr/bin/python
# -*- coding: utf-8 -*-

import boto3
from pprint import pprint
import json
from datetime import datetime, timedelta


def to_timestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6


with open('config.json') as f:
    config = json.load(f)

client = boto3.client('logs', region_name=config['region'])

response = client.describe_log_streams(
    logGroupName=config['log_group_name'],
    orderBy='LastEventTime',
    descending=True,
    limit=config['number_of_log_streams_to_check']
    )

recent_log_streams = []

for log_stream in response['logStreams']:
  last_event_date = datetime.utcfromtimestamp(log_stream['lastEventTimestamp'] / 1000)
  last_event_age = datetime.now() - last_event_date
  if config['log_age_limit_in_seconds'] > last_event_age.total_seconds():
    recent_log_streams.append(log_stream)

for logStream in response['logStreams']:
  response = client.get_log_events(
    logGroupName=config['log_group_name'],
    logStreamName=logStream['logStreamName'],
    startTime=to_timestamp(datetime.utcnow() - timedelta(seconds=config['log_age_limit_in_seconds'])) * 1000 )
  for event in response['events']:
    if config['filter_string'] in event['message']:
      message_dict = json.loads(event['message'])
      print('{} {}'.format(message_dict['timestamp'], message_dict['message'].encode('utf-8')))

