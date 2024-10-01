from jinja2 import Environment, FileSystemLoader
import logging
import paramiko
import io

def execute(ssh_client, params):
    src = params['src']
    dest = params['dest']
    vars = params.get('vars', {})

    # Charger et rendre le template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(src)
    content = template.render(vars)

    try:
        # Utiliser un flux en mémoire pour le contenu rendu
        with io.StringIO(content) as str_io:
            # Créer une commande pour écrire le contenu dans le fichier de destination avec sudo
            command = f"sudo tee {dest} > /dev/null"
            stdin, stdout, stderr = ssh_client.exec_command(command)

            # Écrire le contenu dans stdin de la commande SSH
            stdin.write(str_io.getvalue())
            stdin.channel.shutdown_write()
            
            # Vérifier les erreurs
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                logging.info(f"Template {src} applied to {dest} on remote server.")
            else:
                error_msg = stderr.read().decode()
                logging.error(f"Failed to write template to {dest}: {error_msg}")

    except paramiko.SSHException as e:
        logging.error(f"SSH error occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")