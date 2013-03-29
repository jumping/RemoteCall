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
#import boto.ec2
#import boto.ec2.elb
#import boto.ec2.elb.loadbalancer

DEBUG = False
#DEBUG = True
#connec2 = boto.connect_ec2()
#instance = boto.ec2.instance.Instance(connec2)

#def instance_info(id):
#    instance.id = id
#    try:
#        instance.update()
#        ip_address =  instance.ip_address
#        private_ip = instance.private_ip_address
#        if DEBUG: print ip_address,private_ip
#        return ip_address,private_ip
#    except:
#        return

#def activities_filter(actives):
#    lines = filter(None, actives)
#    instances = {}
#    for line in lines:
#        print line
#        #
#        #print detail messages:
#        #                     line.cause
#        #
#        splited = str(line).split(':')
#        #if splited[0] == 'Activity' and splited[3] == 'Successful progress:100':
#        if splited[0] == 'Activity':
#            #get instance id
#            stat = splited[1].split()
#            (id, flag) = (stat[3], stat[0])
#            if id == 'EC2':
#                id = splited[2].split()[0]
#            if instances.has_key(id):
#                instances[id].append(flag)
#            else:
#                instances[id] = [flag]
#        else:
#            print "Could recognized : %s" %line
#    return instances

#def running_ip(autoscalingname=''):
#    history = []
#    running = []
#    ips = []
#
#    conn = boto.connect_autoscale()
#    groups = conn.get_all_groups()
#    if DEBUG: print len(groups)
#    
#    actives = conn.get_all_activities(autoscalingname)
#    if DEBUG: print actives
#
#    instances = activities_filter(actives)
#    for key in instances.keys():
#        if len(instances[key]) == 2:
#            history.append(key)
#        else:
#            running.append((key,instance_info(key)))
#    if running: 
#        #serving instance public ips
#        for r in running:
#            if r[0] != 'Cannot' and r[-1]:  
#                if DEBUG: print r
#                ips.append(r[-1][0])
#    return ips

def running_ip(autoscalingname='',public=True):
    #history = []
    #running = []
    #ips = []
    
    conn_elb = boto.connect_elb()
    elbname = '-'.join(autoscalingname.split('-')[0:2])
    #conn = boto.connect_autoscale()
    #groups = conn.get_all_groups()
    if DEBUG: print elbname
    
    #actives = conn.get_all_activities(autoscalingname)
    #if DEBUG: print actives

    #lb = boto.ec2.elb.loadbalancer.LoadBalancer(connection=conn, name=elbname)

    #instances = lb.get_instance_health()
    instances = conn_elb.describe_instance_health(elbname)
    instance_ids = [ a.instance_id for a in instances if a.state == u'InService' ]
    conn_ec2 = boto.connect_ec2()
    reservations = conn_ec2.get_all_instances(instance_ids)
    private_ips = [ r.private_ip_address for res in reservations for r in res.instances ]
    public_ips = [ r.ip_address for res in reservations for r in res.instances ]

    #for instance in instances:
    #    if instance.state == u'InService':
    #        running.append((instance,instance_info(instance.instance_id)))
    #if running: 
    #    #serving instance public ips
    #    for r in running:
    #        if r[-1]:  
    #            if DEBUG: print r
    #            ips.append(r[-1][0])
    if public and public_ips:
        return public_ips
    elif private_ips:
        return private_ips
    else:
        return 

def main(autoscalingname):
    #history = []
    #running = []

    #conn = boto.connect_autoscale()
    #groups = conn.get_all_groups()
    #if DEBUG: print len(groups)
    #conn = boto.connect_elb()
    
    #actives = conn.get_all_activities('')
    #if DEBUG: print actives

    #instances = activities_filter(actives)
    #for key in instances.keys():
    #    if len(instances[key]) == 2:
    #        history.append(key)
    #    else:
    #        running.append((key,instance_info(key)))
    #if history: 
    #    print "----------------"
    #    print "History list"
    #    print "----------------"
    #    for h in history:print h
    #print 
    #if running: 
    #    print "----------------"
    #    print "Serving list"
    #    print "----------------"
    #    for r in running:print r 
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
