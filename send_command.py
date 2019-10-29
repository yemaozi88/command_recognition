import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())
client.connect('ev3dev.local', username='robot', password='maker')

stdin, stdout, stderr = client.exec_command('python3 /home/robot/command_recognition/receive_command.py')
#for line in stdout:
#    print(line)

client.close()