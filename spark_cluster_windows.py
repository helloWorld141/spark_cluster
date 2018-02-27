import paramiko

hostname = '144.6.226.7'
port = 22
username = 'ubuntu'
pkey_file = 'C:\\Users\\nghia\\Desktop\\private_keys\\Nectar_Key'

if __name__ == "__main__":
    key = paramiko.RSAKey.from_private_key_file(pkey_file, password='Made565honk')
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()
    s.connect(hostname=hostname, port=port, pkey=key, auth_timeout=60)
    print('ssh connected')
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