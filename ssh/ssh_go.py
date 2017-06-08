
import sys
import os
import socket
import paramiko
from paramiko import SSHClient, SSHException
import StringIO
import datetime
import subprocess

port = 22
time = 5


def key():

    f = open('/home/web/ssh_web/env/ssh_web/key/id_rsa', 'r')
    s = f.read()

    key = paramiko.RSAKey.from_private_key(StringIO.StringIO(s))

    return key


def connect(ip, login, password, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=login, pkey=key(), password=password, port=port, timeout=time)
        shell = ssh.invoke_shell()
    except paramiko.AuthenticationException:
        data = -10
        return data
    except socket.timeout:
        data = -5
        return data


    stdin, stdout, stderr = ssh.exec_command(command)

    data = stdout.read() + stderr.read()

    ssh.close()

    return data


def path(login):

    if login == 'root':
        path = '/' + login + '/.ssh/authorized_keys'
    else:
        path = '/home/' + login + '/.ssh/authorized_keys'

    return path


def add_k(ip, login, password, key):

    sed_add = 'sed -i.bak '
    line_add = '\'$a' + key + '\' '

    command_add = sed_add + line_add + path(login)

    connect(ip, login, password, command_add)



def del_k(ip, login, password, key):

    sed_del = 'sed -i.bak '
    line_del = '\'\#' + key + '#d\' '

    command_del = sed_del + line_del + path(login)

    connect(ip, login, password, command_del)


def check_k(ip, login, password, key):

    # syntax - grep key file | wc -l
    grep = 'grep '
    key = '\'' + key + '\' '
    end = '| wc -l'

    command_check = grep + key + path(login) + end

    data = connect(ip, login, password, command_check)

    return data


def get_info(ip, login, password):   #111 delete

    cat = 'cat '

    command_get = cat + path(login)

    data = connect(ip, login, password, command_get)

    return data


def get_file(ip, login, password):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=login, pkey=key(), password=password, port=port, timeout=time)
    except paramiko.AuthenticationException:
        data = -10
        return data
    except socket.timeout:
        data = -5
        return data

    sftp = ssh.open_sftp()

    filepath = path(login)

    localpath = '/home/web/ssh_web/env/ssh_web/key/remote'

    sftp.get(filepath, localpath)

    data = 0

    ssh.close()

    return data


def save_log(logs, form_key, action):
    f = open('/home/web/ssh_web/env/ssh_web/logs/main', 'a')
    d = datetime.datetime.now()
    data = str(d.strftime("%d-%m-%Y %H:%M"))
    try:
        f.write('---\n')
        f.write(data + '   Action: ' + action)
        f.write('\nKey: ' + form_key + '\n')
        for key, value in logs.items():
            f.write("%s - %s\n" % (key, value))
    finally:
        f.close()


def load():
    f = open('/home/web/ssh_web/env/ssh_web/key/remote', 'r')
    pre_out = []
    out = {}

    try:
        for s in f:
            d = s #.split(' ', 1)
            pre_out.append(d)

        for i, val in enumerate(pre_out):
            out[i] = val

    finally:
        f.close()

    return out