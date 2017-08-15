#!/usr/bin/env python3

import http.client
import json
import os
import urllib

def send_slack_message(text):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    params = urllib.parse.urlencode({
        'payload': json.dumps({
            'text': text
        })
    })

    conn = http.client.HTTPSConnection('hooks.slack.com')
    conn.request('POST', os.environ['WEBHOOK_URL'], params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

def handler(event, context):
    send_slack_message(json.dumps(event, indent=True))
