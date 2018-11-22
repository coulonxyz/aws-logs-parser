# !/usr/bin/python
# -*- coding: utf-8 -*-

import boto3
import json
from datetime import datetime, timedelta
import sys
import getopt
from pprint import pprint

CRED = '\033[91m'
CBLUE = '\033[94m'
CYELLOW = '\033[93m'
CEND = '\033[0m'


class Event:
    def __init__(self, ts, msg):
        self.timestamp = ts
        self.message = msg

    pass


def to_timestamp(dt, epoch=datetime(1970, 1, 1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6


def get_config(env):
    with open('config.json') as f:
        config = json.load(f)
    if env not in config.keys():
        print('Cannot find config env {}. Avalaile are: {}'.format(
            env, config.keys()))
        sys.exit()
    return config[env]


def display_help_and_die():
    print('parser.py -c <config_env>')
    sys.exit()


def get_log_streams(client, log_group_name, log_age_limit):
    recent_log_streams = []
    paginator = client.get_paginator('describe_log_streams')
    response_iterator = paginator.paginate(
        logGroupName=log_group_name,
        logStreamNamePrefix=datetime.utcnow().strftime(
            '%Y/%m/%d/[$LATEST]'),
        descending=False)
    for page in response_iterator:
        for log_stream in page['logStreams']:
            last_event_date = datetime.utcfromtimestamp(
                log_stream['lastEventTimestamp'] / 1000)
            last_event_age = datetime.utcnow() - last_event_date
            if log_age_limit > last_event_age.total_seconds():
                recent_log_streams.append(log_stream)
    recent_log_streams.sort(key=lambda x: x['lastEventTimestamp'], reverse=True)
    return recent_log_streams


def get_events_to_display(client, log_group_name, log_streams, log_age_limit, filter_string):
    events = []
    for logStream in log_streams:
        response = client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=logStream['logStreamName'],
            startTime=to_timestamp(datetime.utcnow() - timedelta(seconds=log_age_limit)) * 1000)
        for event in response['events']:
            if filter_string in event['message'] or filter_string == '*':
                message_dict = json.loads(event['message'])
                events.append(Event(message_dict['timestamp'], message_dict['message']))
    events.sort(key=lambda x: x.timestamp, reverse=False)
    return events


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hc:", ["config-env="])
    except getopt.GetoptError:
        display_help_and_die()
    for opt, arg in opts:
        if opt == '-h':
            display_help_and_die()
        elif opt in ("-c", "--config-env"):
            config = get_config(arg)
        else:
            display_help_and_die()

    client = boto3.client('logs', region_name=config['region'])

    recent_log_streams = get_log_streams(client, config['log_group_name'], config['log_age_limit_in_seconds'])

    events_to_print = get_events_to_display(client, config['log_group_name'],
                                            recent_log_streams,
                                            config['log_age_limit_in_seconds'],
                                            config['filter_string'])

    for event in events_to_print:
        print('{}{}{}\t{}'.format(CBLUE, event.timestamp,
                                  CEND, event.message.encode('utf-8')))


if __name__ == "__main__":
    main(sys.argv[1:])
