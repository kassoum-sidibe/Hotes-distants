import os
import logging
import paramiko

def execute(ssh_client, params):
    src = params['src']
    dest = params['dest']
    backup = params.get('backup', False)

    # Vérifiez si le chemin source existe et s'il s'agit d'un répertoire
    if not os.path.exists(src) or not os.path.isdir(src):
        logging.error(f"Source directory not found or is not a directory: {src}")
        return

    try:
        with ssh_client.open_sftp() as sftp:
            # Créer le répertoire de destination si nécessaire
            try:
                sftp.stat(dest)
            except IOError:
                sftp.mkdir(dest)

            # Parcourir les fichiers dans le répertoire source
            for item in os.listdir(src):
                path_src = os.path.join(src, item)
                path_dest = os.path.join(dest, item)

                if os.path.isfile(path_src):
                    # Gérer la sauvegarde si nécessaire
                    if backup:
                        try:
                            sftp.stat(path_dest)
                            sftp.rename(path_dest, path_dest + ".backup")
                        except IOError:
                            # Si le fichier n'existe pas déjà, aucune sauvegarde n'est nécessaire
                            pass

                    # Copier le fichier
                    sftp.put(path_src, path_dest)
                    logging.info(f"File copied: {path_src} to {path_dest}")

    except paramiko.SSHException as e:
        logging.error(f"SSH error occurred while copying: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while copying: {e}")