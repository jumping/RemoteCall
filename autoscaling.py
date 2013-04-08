#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   Jumping Qu @ BPO
#
#vim: ts=4 sts=4 et sw=4
#
"""
autoscaling.py
"""

import boto

DEBUG = False
#DEBUG = True

def running_ip(autoscalingname='',public=True):
    
    conn_elb = boto.connect_elb()
    elbname = '-'.join(autoscalingname.split('-')[0:2])
    if DEBUG: print elbname
    
    instances = conn_elb.describe_instance_health(elbname)
    instance_ids = [ a.instance_id for a in instances if a.state == u'InService' ]
    conn_ec2 = boto.connect_ec2()
    reservations = conn_ec2.get_all_instances(instance_ids)
    private_ips = [ r.private_ip_address for res in reservations for r in res.instances ]
    public_ips = [ r.ip_address for res in reservations for r in res.instances ]

    if public and public_ips:
        return public_ips
    elif private_ips:
        return private_ips
    else:
        return 

def main(autoscalingname):
    print ' '.join(running_ip(autoscalingname))

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options]")
    parser.add_option("-n", "--name", help="The name of ASG", dest="name")
    parser.add_option("-p", "--private_ip", action="store_true", help="output private ip", dest="private_ip")
    (options, args) = parser.parse_args()
    if options.name:
        if options.private_ip:
            print ' '.join(running_ip(options.name, False))
        else:
            main(options.name)
