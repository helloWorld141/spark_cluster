import paramiko, json

port = 22

def exe(ssh, cmd, arg=""):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("Remote stdout:\n" + stdout.read().decode('utf-8'))
    print("Remote stderr:\n" + stderr.read().decode('utf-8'))
    return stdin, stdout, stderr

def editHosts(ssh):
    exec(ssh, "sudo nano /etc/hosts")

class ssh:
        shell = None
            client = None
                transport = None

                    def __init__(self, address, username, password):
                                print("Connecting to server on ip", str(address) + ".")
                                        self.client = paramiko.client.SSHClient()
                                                self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
                                                        self.client.connect(address, username=username, password=password, look_for_keys=False)
                                                                self.transport = paramiko.Transport((address, 22))
                                                                        self.transport.connect(username=username, password=password)

                                                                                thread = threading.Thread(target=self.process)
                                                                                        thread.daemon = True
                                                                                                thread.start()

                                                                                                    def closeConnection(self):
                                                                                                                if(self.client != None):
                                                                                                                                self.client.close()
                                                                                                                                            self.transport.close()

                                                                                                                                                def openShell(self):
                                                                                                                                                            self.shell = self.client.invoke_shell()

                                                                                                                                                                def sendShell(self, command):
                                                                                                                                                                            if(self.shell):
                                                                                                                                                                                            self.shell.send(command + "\n")
                                                                                                                                                                                                    else:
                                                                                                                                                                                                                    print("Shell not opened.")

                                                                                                                                                                                                                        def process(self):
                                                                                                                                                                                                                                    global connection
                                                                                                                                                                                                                                            while True:
                                                                                                                                                                                                                                                            # Print data when available
                                                                                                                                                                                                                                                                        if self.shell != None and self.shell.recv_ready():
                                                                                                                                                                                                                                                                                            alldata = self.shell.recv(1024)
                                                                                                                                                                                                                                                                                                            while self.shell.recv_ready():
                                                                                                                                                                                                                                                                                                                                    alldata += self.shell.recv(1024)
                                                                                                                                                                                                                                                                                                                                                    strdata = str(alldata, "utf8")
                                                                                                                                                                                                                                                                                                                                                                    strdata.replace('\r', '')
                                                                                                                                                                                                                                                                                                                                                                                    print(strdata, end = "")
                                                                                                                                                                                                                                                                                                                                                                                                    if(strdata.endswith("$ ")):
                                                                                                                                                                                                                                                                                                                                                                                                                            print("\n$ ", end = "")


                                                                                                                                                                                                                                                                                                                                                                                                                            sshUsername = "SSH USERNAME"
                                                                                                                                                                                                                                                                                                                                                                                                                            sshPassword = "SSH PASSWORD"
                                                                                                                                                                                                                                                                                                                                                                                                                            sshServer = "SSH SERVER ADDRESS"


                                                                                                                                                                                                                                                                                                                                                                                                                            connection = ssh(sshServer, sshUsername, sshPassword)
                                                                                                                                                                                                                                                                                                                                                                                                                            connection.openShell()
                                                                                                                                                                                                                                                                                                                                                                                                                            while True:
                                                                                                                                                                                                                                                                                                                                                                                                                                    command = input('$ ')
                                                                                                                                                                                                                                                                                                                                                                                                                                        if command.startswith(" "):
                                                                                                                                                                                                                                                                                                                                                                                                                                                    command = command[1:]
                                                                                                                                                                                                                                                                                                                                                                                                                                                        connection.sendShell(command)

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
    #stdin, stdout, stderr = editHosts(s)
    s.close()
