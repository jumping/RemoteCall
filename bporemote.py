#!/usr/bin/env python
# -*- coding: UTF8 -*-
# 
#   Jumping Qu @ BPO
#
#vim: ts=4 sts=4 et sw=4
#
"""
bporemote.py
"""
import os
import paramiko
#import cmd

DEBUG=False

def uniqify_seq(seq):
    set = {}
    map(set.__setitem__, seq, [])
    return set.keys()

class Remote(object):
    """
    package paramiko
    """
    def __init__(self):
        #cmd.Cmd.__init__(self)
        self.hosts = []
        self.connections = []

    def __connect(self, hname, uname='root', ssh_key='/root/bpo.pem'):
        """
        connect to all hosts in hosts list
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname = hname, username=uname, key_filename=ssh_key)
        self.ssh.use_sudo = False
        self.connections.append(self.ssh)

    def add_host(self, newhost):
        """
        add_host(host)
        will add host to hosts list
        """
        self.hosts.append(newhost)
        self.__connect(newhost)

    def run_once(self, cmd):
        """
        runcmd at remote host
        """
        result = { 'stdout': [], 'stderr': [] }
        if cmd:
            for host, conn in zip(self.hosts, self.connections):

                stdin, stdout, stderr = conn.exec_command(cmd)
                stdin.close()

                result['stdout'].append(stdout.read())
                result['stderr'].append(stderr.read())

                #for line in result['stdout'].splitlines():
                #    print 'host: %s: %s' % (host, line)
                if DEBUG:
                    print host
                    print result
                    print

            for k in result:
                result[k] = uniqify_seq(result[k])
                if '' in result[k]:
                    result[k].remove('')

            return result
        else:
            print "No command!"

    def run_more(self, ssh, cmd, check_exit_status=True):
        """
        run multi cmds at remote host by transport
        """
        chan = ssh.get_transport().open_session()
        stdin = chan.makefile('wb') 
        stdout = chan.makefile('rb')
        stderr = chan.makefile_stderr('rb')
        processed_cmd = cmd
        if ssh.use_sudo:
            processed_cmd = 'sudo -S bash -c "%s"' % cmd.replace('"', '\\"')
        chan.exec_command(processed_cmd)
        if stdout.channel.closed is False:
            print "Channel closed."
            return

        result = { 'stdout': [], 'stderr': [] }

        exit_status = chan.recv_exit_status()
        result['exit_status'] = exit_status
        for line in stdout: result['stdout'].append(line)
        for line in stdout: result['stdout'].append(line)

        if check_exit_status and exit_status != 0:
            print "The following cmds has error."
            print cmd
            print "Error messages: %s" % result['stderr']

        return result
            
    def run_cmds_hosts(self, cmd, check_exit_status=True):
        """
        run multi cmds on known hosts
        """
        results = {}
        for host, conn in zip(self.hosts, self.connections):
            results[host] = self.run_more(conn, cmd, check_exit_status)

        for k in result:
            result[k] = utils.uniqify_seq(result[k])
        return results
            
    def put(self, localfile, remotefile):
        """
        put file from localhost to  remote machine
        """
        if not os.path.exists(localfile):
            print "Please make sure %s exists!" % localfile
            return

        if os.path.isdir(remotefile):
            """
            if remotefile is a directory, then will consist 
            the path of remotefile 
            with 
            remotefile  + basename(localfile)
            """
            remotefile = os.path.join(remotefile, os.path.basename(localfile))

        for host, conn in zip(self.hosts, self.connections):
            ftp = conn.open_sftp()
            ftp.put(localfile, remotefile)
            ftp.close()

    def get(self, remotefile, localfile):
        """
        download file from remote machine
        """
        if os.path.exists(localfile):
            print "The %s exists!" % localfile
            return
        for host, conn in zip(self.hosts, self.connections):
            ftp = conn.open_sftp()
            ftp.get(remotefile, localfile)
            ftp.close()

    def close(self):
        """
        close connection, and empty self.hosts and self.connections
        """
        for conn in self.connections:
            conn.close()
        self.hosts = []
        self.connections = []

if __name__ == '__main__':
    remote = Remote() 
    remote.add_host('127.0.0.1')
    cmds = """
    pwd
    cd /var/log
    pwd
    ls -la
    """

    remote.run_cmds_hosts(cmds)
