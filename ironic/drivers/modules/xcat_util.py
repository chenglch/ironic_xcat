__author__ = 'chenglong'

import paramiko
import time
from ironic.openstack.common import log as logging
from oslo.config import cfg

xcat_opts = [
    cfg.StrOpt('network_node_ip',
               default='127.0.0.1',
               help='IP address of neutron network node'),
    cfg.StrOpt('ssh_user',
               default='root',
               help='Username of neutron network node.'),
    cfg.StrOpt('ssh_password',
               default='cluster',
               help='Password of neutron network node'),
    cfg.IntOpt('ssh_login_wait',
               default=3,
               help='Sleep time of ssh login'),
    cfg.IntOpt('ssh_session_timeout',
               default=10,
               help='ssh session time'),
    cfg.IntOpt('ssh_shell_wait',
               default=1,
               help='wait time for the ssh cmd excute'),
    cfg.IntOpt('ssh_port',
               default=22,
               help='ssh connection port for the neutron '),
    cfg.IntOpt('ssh_buf_size',
               default=65535,
               help='Maximum size (in charactor) of cache for ssh, '
               'including those in use'),
    ]

LOG = logging.getLogger(__name__)

CONF = cfg.CONF
CONF.register_opts(xcat_opts, group='xcat')


ssh_login_wait = 3
ssh_session_timeout = 10
ssh_shell_wait = 1

username = 'ubuntu'
password = 'cluster'
buf_size = 65535

def xcat_ssh(ip,port,username,password,cmd):
    t = paramiko.Transport((ip,port))
    t.connect(username = username ,password = password )
    chan=t.open_session()
    chan.settimeout(CONF.xcat.ssh_session_timeout)
    chan.get_pty()
    chan.invoke_shell()
    time.sleep(CONF.xcat.ssh_login_wait)
    chan.recv(buf_size)
    for  c in cmd :
        _xcat_ssh_exec(chan,c,password)



def _xcat_ssh_exec(chan,cmd,password):
    chan.send(cmd + '\n')
    time.sleep(CONF.xcat.ssh_shell_wait)
    ret = chan.recv(buf_size)
    print ret
    if 'password' in ret and ret.rstrip().endswith(':'):
        chan.send(password + '\n')
        ret = chan.recv(CONF.xcat.ssh_buf_size)
    return ret

def _tsplit(string, delimiters):
        """Behaves str.split but supports multiple delimiters."""
        delimiters = tuple(delimiters)
        stack = [string,]
        for delimiter in delimiters:
            for i, substring in enumerate(stack):
                substack = substring.split(delimiter)
                stack.pop(i)
                for j, _substring in enumerate(substack):
                    stack.insert(i+j, _substring)
        return stack