#!/usr/bin/env python
# -*- coding: UTF8 -*-
import boto
import boto.ec2
import boto.ec2.elb
import boto.ec2.elb.loadbalancer

DEBUG = False
#DEBUG = True
connec2 = boto.connect_ec2()
instance = boto.ec2.instance.Instance(connec2)

def instance_info(id):
    instance.id = id
    try:
        instance.update()
        ip_address =  instance.ip_address
        private_ip = instance.private_ip_address
        if DEBUG: print ip_address,private_ip
        return ip_address,private_ip
    except:
        return

def activities_filter(actives):
    lines = filter(None, actives)
    instances = {}
    for line in lines:
        print line
        #
        #print detail messages:
        #                     line.cause
        #
        splited = str(line).split(':')
        #if splited[0] == 'Activity' and splited[3] == 'Successful progress:100':
        if splited[0] == 'Activity':
            #get instance id
            stat = splited[1].split()
            (id, flag) = (stat[3], stat[0])
            if id == 'EC2':
                id = splited[2].split()[0]
            if instances.has_key(id):
                instances[id].append(flag)
            else:
                instances[id] = [flag]
        else:
            print "Could recognized : %s" %line
    return instances

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

def running_ip(autoscalingname=''):
    history = []
    running = []
    ips = []
    
    conn = boto.connect_elb()
    elbname = '-'.join(autoscalingname.split('-')[0:2])
    #conn = boto.connect_autoscale()
    #groups = conn.get_all_groups()
    if DEBUG: print elbname
    
    #actives = conn.get_all_activities(autoscalingname)
    #if DEBUG: print actives

    lb = boto.ec2.elb.loadbalancer.LoadBalancer(connection=conn, name=elbname)

    instances = lb.get_instance_health()
    for instance in instances:
        if instance.state == u'InService':
            running.append((instance,instance_info(instance.instance_id)))
    if running: 
        #serving instance public ips
        for r in running:
            if r[-1]:  
                if DEBUG: print r
                ips.append(r[-1][0])
    return ips

def main():
    history = []
    running = []

    #conn = boto.connect_autoscale()
    #groups = conn.get_all_groups()
    #if DEBUG: print len(groups)
    conn = boto.connect_elb()
    
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
    print running_ip()

if __name__ == '__main__':
    main()
