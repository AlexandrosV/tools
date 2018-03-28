#!/usr/bin/python


import os
import json
import yaml
import requests
import datetime
from time import sleep
# Python 2.6
from ordereddict import OrderedDict
# Python 2.7
# From collections import OrderedDict
from requests.auth import HTTPBasicAuth


class Configuration(object):
    user = ""
    passwd = ""

    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd


def setArguments(arguments):

    # Here implement any logic needed on arguments
    return arguments


def setParameters():
    
    workspace = os.path.dirname(os.path.realpath(__file__))
    conf_file = workspace + '/settings.yml'
    parameters = yaml.load(open(conf_file))
    user = parameters['USER']
    passwd = parameters['PASSWD']
    configuration = Configuration(user, passwd)
    try:
        arguments = parameters['PARAMETERS']
        setArguments(arguments)
    except LookupError:
        pass
    return configuration


def sendGetRequest(uri, user, psswd):
    response = requests.get(uri, auth=HTTPBasicAuth(user, psswd))
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)
        return "Error"


def sendPostRequest(uri, user, psswd, payload):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(uri, auth=HTTPBasicAuth(user, psswd),
                             headers=headers, data=json.dumps(payload))
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        return data
    else:
        print(response.text)
        print(response.status_code)
        return "Error"


if __name__ == '__main__':
    # Delete me!
    repor_slug = ""
    conf = setParameters()

    # Define API uri
    base_uri = "https://api.bitbucket.org/2.0/repositories/.../"
    base_uri += repo_slug + "/pipelines/"

    # Set payload
    payload = OrderedDict()
    target = OrderedDict()
