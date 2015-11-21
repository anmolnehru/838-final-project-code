import os
import paramiko


def get_private_key():
    # or choose the location and the private key file on your client
    private_key_file = os.path.expanduser("/home/ubuntu/.ssh/id_rsa")
    return paramiko.RSAKey.from_private_key_file(private_key_file, password='')


def get_ssh(myusername, myhostname, myport):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(myhostname, username=myusername, port=myport, pkey = private_key)
    ssh.connect(myhostname, username=myusername, port=myport)
    return ssh

def block_exec(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    return

def clear_bw_config2(ssh, interface):
    block_exec(ssh, "sudo tc qdisc del dev %s root" % interface)
    block_exec(ssh, "sudo tc qdisc del dev %s ingress" % interface)
    block_exec(ssh, "sudo tc class del dev %s root" % interface)
    block_exec(ssh, "sudo tc filter del dev %s root" % interface)


def exec_bw_config2(ssh, interface, bandwidth, ip, subnetmasklength):
    clear_bw_config2(ssh, interface)
    # create a qdisc (queuing discipline), 12 is default class
    cmd1 = "sudo tc qdisc add dev %s root handle 1: htb default 12" % interface
    print cmd1
    block_exec(ssh, cmd1)

    # define the performance for default class
    cmd2 = "sudo tc class add dev %s parent 1: classid 1:1 htb rate %dmbps ceil %dmbps" % (interface, bandwidth, bandwidth )
    print cmd2

    block_exec(ssh, cmd2)


    filter_cmd = "sudo tc filter add dev %s protocol ip parent 1:0 prio 1 u32 match ip dst %s/%d flowid 1:1" % (interface, ip, subnetmasklength)
    print filter_cmd
    block_exec(ssh, filter_cmd)

def main():
    myhosts = ["10.0.1.193",  "10.0.1.192", "10.0.1.191", "10.0.1.190"]
    username="ubuntu"
    port=22
    #key = ""get_private_key()
    for host in myhosts:
    	ssh = get_ssh(username, host, port)
	clear_bw_config2(ssh, "eth0")
	exec_bw_config2(ssh, "eth0", 128, "10.0.0.0", 8)

    # iterate over hosts here
    # for everyhost,
    # 1. create ssh connection
    # 2. run the exec_bw_config with params
    return

if __name__ == '__main__':
    main()
