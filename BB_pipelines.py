#!/usr/bin/python


import os
import json
import requests
import datetime
from time import sleep
# Python 2.6
from ordereddict import OrderedDict
# Python 2.7
# From collections import OrderedDict
from requests.auth import HTTPBasicAuth


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


def checkPipeline(base_uri, user, psswd, uuid):
    count = 0
    uri = base_uri + uuid
    while True:
        response = sendGetRequest(uri, user, psswd)
        state = response["state"]["name"]
        if state == "COMPLETED":
            print "\nCOMPLETED:",
            return response
        else:
            sleep(1)
            count = count + 1
            if count > 80:
                print "\n"
                count = 0
            print ".",


# MAIN ()
if __name__ == '__main__':
    # Read arguments (for future use)
    # repo_slug = sys.argv[1]
    # branch = sys.argv[2]
    # commit_hash = sys.argv[3]

    # Read credentials
    user = os.environ['user']
    password = os.environ['password']

    # Delete me!
    repo_slug = "xxxxxxxxx"
    branch = "master"

    # Define API URI
    base_uri = "https://api.bitbucket.org/2.0/repositories/xxxxxxxxx/"
    base_uri += repo_slug + "/pipelines/"

    # Set payload
    payload = OrderedDict()
    target = OrderedDict()
    # To trigger pipelines for a commit
    # commit = OrderedDict()
    # commit["type"] = "commit"
    # commit["hash"] = "commit_hash"
    # target["commit"] = commit
    target["ref_type"] = "branch"
    target["type"] = "pipeline_ref_target"
    # Change me
    target["ref_name"] = branch
    payload["target"] = target
    # Execute Pipeline
    response = sendPostRequest(base_uri, user, password, payload)
    # If successful buil, print Report
    if response != "Error":
        uuid = response["uuid"]
        repository = response["repository"]["name"]
        branch = response["target"]["ref_name"]
        print "Building: %s - %s branch\n" % (repository, branch)
        # Wait for pipeline to finish
        response = checkPipeline(base_uri, user, password, uuid)
        # Read response
        build_number = response["build_number"]
        commit_hash = response["target"]["commit"]["hash"]
        pipeline = response["uuid"]
        duration = response["build_seconds_used"]
        finish_date = response["completed_on"]
        status = response["state"]["result"]["name"]
        html = response["repository"]["links"]["html"]["href"]
        logs = str(html) + "/addon/pipelines/home#!/results/"
        logs += str(build_number)
        print "%s (%s)" % (status, finish_date)
        print "Build Number: %s" % (build_number)
        print "Duration: %s" % (str(datetime.timedelta(seconds=int(duration))))
        print "Commit: %s" % (commit_hash)
        print "Pipeline: %s" % (pipeline)
        print "Logs: %s" % (logs)
