import logging
import paramiko

def execute(ssh_client, params):
    command = params['command']
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()  # Bloquant jusqu'à ce que la commande soit terminée
        if exit_status == 0:
            logging.info(f"Commande réussie: {command}")
        else:
            logging.error(f"Erreur dans la commande {command}: {stderr.read().decode('utf-8')}")
    except Exception as e:
        logging.error(f"Exception lors de l'exécution de la commande {command}: {e}")