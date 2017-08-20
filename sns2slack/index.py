#!/usr/bin/env python3

import collections
import datetime
import http.client
import json
import os
import urllib

def send_slack_message(payload):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }

    params = urllib.parse.urlencode({
        'payload': json.dumps(payload)
    })

    conn = http.client.HTTPSConnection('hooks.slack.com')
    conn.request('POST', os.environ['WEBHOOK_URL'], params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

def parse_timestamp(timestamp):
    return datetime.datetime.strptime(
        timestamp,
        '%Y-%m-%dT%H:%M:%S.%fZ'
    ).replace(tzinfo=datetime.timezone.utc)

def format_value(value, prefix=''):
    result = ''
    if isinstance(value, dict):
        for k, v in value.items():
            result += format_value(v, prefix + '.' + k if prefix else k)
    elif isinstance(value, list):
        for k, v in enumerate(value):
            result += format_value(v, prefix + '[{}]'.format(k) if prefix else '[{}]'.format(k))
    else:
        if prefix:
            result = '{}: {}\n'.format(prefix, value)
        else:
            result = value
    return result

def format_message(event):
    attachment = {}
    attachment['title'] = event['Records'][0]['Sns']['Subject']
    attachment['ts'] = parse_timestamp(event['Records'][0]['Sns']['Timestamp']).timestamp()

    try:
        message = json.loads(
            event['Records'][0]['Sns']['Message'],
            object_pairs_hook=collections.OrderedDict
        )

        if 'AlarmName' in message:
            if message['NewStateValue'] == 'ALARM':
                attachment['color'] = 'danger'
            elif message['NewStateValue'] == 'OK':
                attachment['color'] = 'good'

        attachment['fields'] = []

        for key, value in message.items():
            attachment['fields'].append({
                'title': key,
                'value': format_value(value),
            })
    except json.decoder.JSONDecodeError:
        attachment['text'] = event['Records'][0]['Sns']['Message']

    return {'attachments': [attachment]}

def handler(event, context):
    print(event)
    payload = format_message(event)
    send_slack_message(payload)
