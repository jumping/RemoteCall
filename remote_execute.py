#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   Jumping Qu @ BPO
#
#vim: ts=4 sts=4 et sw=4
#
"""
remote_execute.py
"""

impor tlogging
import bporemote
import autoscaling
import datetime


def execute(as_name, cmdline, app):
    hosts = autoscaling.running_ip(as_name,True)
    #hosts = ['10.244.14.224']
    now = datetime.datetime.now()
    file_handler = logging.FileHandler('/tmp/execute.log')
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('starting %s\n' % now)
    app.logger.info('%s\n' % str(hosts))
    hostobj = bporemote.Remote()
    for host in hosts:
        app.logger.info(host)
        hostobj.add_host(host)
    output =  hostobj.run_once(cmdline)
    now = datetime.datetime.now()
    app.logger.info(str(output))
    app.logger.info('end @ %s\n' % now)
    return output

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options]")
    parser.add_option("-n", "--asname", help="The name of autoscaling", dest="as_name")
    parser.add_option("-c", "--cmd", help="The cmd will execute remotely", dest="cmdline")
    (options, args) = parser.parse_args()
    if not options.cmdline or not options.as_name :
        import sys
        print "Please check the input"
        sys.exit(1)
    execute(options.as_name, options.cmdline)
