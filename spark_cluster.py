import paramiko, json

port = 22

if __name__ == "__main__":
    file = open('spark_cluster.conf').read()
    config = json.loads(file)
    pkey_file = config['pkey']
    master = config['hosts']['master']
    slaves = config['hosts']['slaves']
    username = config['username']
    print(slaves, master)
    ######
    key = paramiko.RSAKey.from_private_key_file(pkey_file, password='Made565honk')
    print(key)
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()
    s.connect(slaves[0], port, pkey=key, auth_timeout=60)
    print('ssh connected')
    ######
    stdin, stdout, stderr = s.exec_command('ifconfig')
    print(stderr.read())
    print("Remote stdout:\n" + stdout.read().decode('utf-8'))
    print("Remote stderr:\n" + stderr.read().decode('utf-8'))
    if stderr.read() != b'':
        stdin, stdout, stderr = s.exec_command('sudo apt-get install net-tools')
    print('command executed')
    print("Remote stdout:\n" + stdout.read().decode('utf-8'))
    print("Remote stderr:\n" + stderr.read().decode('utf-8'))
    s.close()
