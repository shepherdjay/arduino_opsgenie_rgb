#!/usr/bin/python

import sys
import time
import ConfigParser

import requests

sys.path.insert(0, '/usr/lib/python2.7/bridge')
from bridgeclient import BridgeClient as bridgeclient

API_ALERTS_URL = "https://api.opsgenie.com/v2/alerts"
API_INCIDENTS_URL = 'https://api.opsgenie.com/v1/incidents'

with open('/mnt/sda1/pythonfiles/opsgeniergb/apikey.cfg', 'r') as configfile:
    config = ConfigParser.ConfigParser()
    config.readfp(configfile)

API_KEY = "GenieKey {}".format(config.get('DEFAULT', 'GENIEKEY'))


def get_environment_status():
    # Get right now
    currentUnixStamp = int(time.time())

    # Common Headers
    headers = {'Authorization': API_KEY}

    # Check for Incidents and return CRITICAL if found
    parameters = {'query': 'status:open'}
    incidents = requests.get(API_INCIDENTS_URL, headers=headers, params=parameters).json()['data']
    if len(incidents) > 0:
        return "CRITICAL"

    # Check for Recent Alerts and return WARNING if found
    parameters = {'query': 'status:open AND createdAt>={})'.format(currentUnixStamp - 86400)}
    alerts = requests.get(API_ALERTS_URL, headers=headers, params=parameters).json()['data']
    if len(alerts) > 0:
        return "WARNING"

    # Check for open alerts not yet closed
    parameters = {'query': 'status:open'}
    alerts = requests.get(API_ALERTS_URL, headers=headers, params=parameters).json()['data']
    if len(alerts) > 0:
        return "INFO"

    return "NORMAL"


def find_color():
    color_mapping = {
        "CRITICAL": "RED",
        "WARNING": "YELLOW",
        "INFO": "BLUE",
        "NORMAL": "GREEN"
    }

    return color_mapping[get_environment_status()]


def write_arduino(color):
    color_to_rgb_map = {
        "RED": ("255", "0", "0"),
        "YELLOW": ("255", "255", "0"),
        "GREEN": ("0", "255", "0"),
        "BLUE": ("0", "0", "255"),
    }
    pythonRed, pythonGreen, pythonBlue = color_to_rgb_map[color]
    bridge = bridgeclient()
    bridge.put('pythonRed', pythonRed)
    bridge.put('pythonGreen', pythonGreen)
    bridge.put('pythonBlue', pythonBlue)


if __name__ == '__main__':
    color = find_color()
    write_arduino(color)
