import logging

def execute(ssh_client, params):
    name = params['name']
    state = params['state']

    command = f"sudo systemctl {state} {name}"
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    if exit_status == 0:
        logging.info(f"Service {name} is now {state}.")
    else:
        logging.error(f"Error managing service {name}: {stderr.read().decode()}")
