import logging
import paramiko

def execute(ssh_client, params):
    name = params['name']
    state = params['state']

    # Construction de la commande apt
    if state == "present":
        command = f"sudo apt-get install -y {name}"
    elif state == "absent":
        command = f"sudo apt-get remove -y {name}"
    else:
        logging.error(f"Unknown state '{state}' for package {name}")
        return

    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            logging.info(f"Package {name} is now {state}.")
        else:
            stderr_output = stderr.read().decode()
            logging.error(f"Error with package {name}: {stderr_output}")
    except paramiko.SSHException as e:
        logging.error(f"SSH error occurred while executing apt command: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while executing apt command: {e}")