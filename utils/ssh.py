import paramiko
import logging

def connect(host_details):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if 'ssh_key_file' in host_details:
            client.connect(
                hostname=host_details['ssh_address'],
                port=host_details['ssh_port'],
                username=host_details.get('ssh_user'),
                key_filename=host_details['ssh_key_file']
            )
        elif 'ssh_password' in host_details:
            client.connect(
                hostname=host_details['ssh_address'],
                port=host_details['ssh_port'],
                username=host_details.get('ssh_user'),
                password=host_details['ssh_password']
            )
        else:
            client.connect(
                hostname=host_details['ssh_address'],
                port=host_details['ssh_port'],
                username=host_details.get('ssh_user')
            )
        return client
    except paramiko.AuthenticationException:
        logging.error(f"Authentication failed when connecting to {host_details['ssh_address']}")
        return None
    except paramiko.SSHException as e:
        logging.error(f"SSH error occurred while connecting to {host_details['ssh_address']}: {e}")
        return None