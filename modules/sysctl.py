import logging
import paramiko

def execute(ssh_client, params):
    attribute = params['attribute']
    value = params['value']
    permanent = params.get('permanent', False)

    try:
        # Exécuter la commande sysctl pour modifier le paramètre
        command = f"sudo sysctl -w {attribute}={value}"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status != 0:
            logging.error(f"Error setting sysctl {attribute}: {stderr.read().decode()}")
            return

        # Rendre la modification permanente si nécessaire
        if permanent:
            echo_command = f"echo '{attribute}={value}' | sudo tee -a /etc/sysctl.conf"
            stdin, stdout, stderr = ssh_client.exec_command(echo_command)
            exit_status = stdout.channel.recv_exit_status()

            if exit_status == 0:
                logging.info(f"Sysctl {attribute} permanently set to {value}.")
            else:
                logging.error(f"Failed to make sysctl {attribute} permanent: {stderr.read().decode()}")

    except paramiko.SSHException as e:
        logging.error(f"SSH error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")