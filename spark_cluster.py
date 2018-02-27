import paramiko, json

port = 22

def exe(ssh, cmd, arg=""):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("Remote stdout:\n" + stdout.read().decode('utf-8'))
    print("Remote stderr:\n" + stderr.read().decode('utf-8'))
    return stdin, stdout, stderr

def editHosts(ssh, master):
    stdin, stdout, stderr = exec(ssh, "sudo nano /etc/hosts")
    stdin.write("MASTER-IP " + master)

if __name__ == "__main__":
    file = open('spark_cluster.conf').read()
    config = json.loads(file)
    pkey_file = config['pkey']
    master = config['hosts']['master']
    slaves = config['hosts']['slaves']
    username = config['username']
    ######
    key = paramiko.RSAKey.from_private_key_file(pkey_file, password='Made565honk')
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()
    s.connect(slaves[0], port, pkey=key, auth_timeout=60)
    print('ssh connected')
    ######
    stdin, stdout, stderr = exe(s, 'ifconfig')
    if stderr.read() != b'':
        stdin, stdout, stderr = exe(s, 'sudo apt-get install net-tools; ifconfig')
    stdin, stdout, stderr = editHosts(s, master)
    s.close()
