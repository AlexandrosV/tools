#!/usr/bin/python


import os
import sys
import yaml
import jenkins
from time import sleep


class Configuration(object):
    user = ""
    passwd = ""
    server = ""

    def __init__(self, user, passwd, server, pipeline, load, delay):
        self.user = user
        self.passwd = passwd
        self.server = server
        self.pipeline = pipeline
        self.load = load
        self.delay = delay


def setConfigurations():
    workspace = os.path.dirname(os.path.realpath(__file__))
    conf_file = workspace + '/settings.yml'
    configurations = yaml.load(open(conf_file))
    user = configurations['USER']
    passwd = configurations['PASSWD']
    server = configurations['SERVER']
    pipeline = configurations['PIPELINE']
    load = configurations['LOAD']
    delay = configurations['DELAY_BETWEEN_BUILDS']

    configuration = Configuration(user, passwd, server, pipeline, load, delay)
    return configuration


def setParameters():
    parameters = {}
    workspace = os.path.dirname(os.path.realpath(__file__))
    conf_file = workspace + '/settings.yml'
    configurations = yaml.load(open(conf_file))
    parameters['branch'] = configurations['BRANCH']
    # Add as much parameters as needed
    # parameters['NPM_VAR2'] = configurations['NPM_VAR2']
    return parameters


if __name__ == '__main__':
    conf = setConfigurations()
    server = jenkins.Jenkins(conf.server, username=conf.user,
                             password=conf.passwd)
    # To test conection to server
    # user = server.get_whoami()
    # version = server.get_version()
    # print('Hello %s from Jenkins %s' % (user['fullName'], version))

    # Pipeline parameters
    params = setParameters()
    # Trigger pipelines
    load = 0
    builds = []
    while load < conf.load:
        load = load + 1
        builds.append(server.get_job_info(conf.pipeline)['nextBuildNumber'])
        server.build_job(conf.pipeline, params)
        sleep(conf.delay)
    print('Builds: %s ' % (builds))

    # Monitor pipelines
    for job in builds:
        while True:
            # Stetics
            sys.stdout.write('.')
            sys.stdout.flush()
            # Check build status
            output = server.get_build_info(conf.pipeline, job)
            state = str(output['building'])
            if state == "False":
                break
            sleep(0.5)
        print('\n Pipeline completed: %s \n' % (output))
