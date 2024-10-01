import argparse
import yaml
import logging
from utils import ssh
from modules import copy, template, service, sysctl, apt, command

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_args():
    parser = argparse.ArgumentParser(description='MyLittleAnsible CLI tool')
    parser.add_argument('-i', '--inventory', required=True, help='Inventory YAML file')
    parser.add_argument('-f', '--file', required=True, help='Playbook YAML file')
    return parser.parse_args()

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error loading YAML file {file_path}: {e}")
        raise

def main():
    args = parse_args()
    inventory = load_yaml(args.inventory)
    todos = load_yaml(args.file)
    
    for host_name, host_details in inventory['hosts'].items():
        logging.info(f"Processing host: {host_name}")
        try:
            with ssh.connect(host_details) as client:
                for todo in todos:
                    module = todo['module']
                    params = todo['params']

                    if module == 'copy':
                        copy.execute(client, params)
                    elif module == 'template':
                        template.execute(client, params)
                    elif module == 'service':
                        service.execute(client, params)
                    elif module == 'sysctl':
                        sysctl.execute(client, params)
                    elif module == 'apt':
                        apt.execute(client, params)
                    elif module == 'command':
                        command.execute(client, params)
                    else:
                        logging.warning(f"Unknown module: {module}")

        except Exception as e:
            logging.error(f"Failed to process host {host_name}: {e}")

        logging.info(f"Completed processing host: {host_name}")

if __name__ == "__main__":
    main()