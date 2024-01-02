#!/usr/bin/env python3
import argparse
import os
import yaml
import subprocess

CONFIG_DIR = os.path.expanduser('~/.config/pwna')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'pwna.yaml')


def ensure_config_directory_exists():
    """Ensure the configuration directory exists."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        return False
    return True


def generate_default_config():
    """Generate a default config file."""
    default_config = {
        'http_directory': './http_server_directory',
        'http_port': 8000
    }
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(default_config, f)
    print(f"Default config file '{CONFIG_FILE}' generated.")
    exit()


def load_config():
    """Load configuration from the config file."""
    if not ensure_config_directory_exists():
        generate_default_config()
    
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)


def create_symlink(http_directory):
    """Create a symlink for the current directory in the specified http_directory."""
    cwd = os.getcwd()
    symlink_path = os.path.join(http_directory, os.path.basename(cwd))
    if not os.path.exists(symlink_path):
        os.symlink(cwd, symlink_path)


def start_http_server(http_directory, http_port):
    """Start an HTTP server in the specified directory and port."""
    os.chdir(http_directory)
    subprocess.run(['python3', '-m', 'http.server', str(http_port)])


def main():
    if not ensure_config_directory_exists():
        print("No config file found. A default config will be generated.")
        generate_default_config()

    parser = argparse.ArgumentParser(description='Sample script with argparse')
    
    # Add subparsers
    subparsers = parser.add_subparsers(dest='module')
    
    # Create http subparser
    http_parser = subparsers.add_parser('http', help='HTTP module')
    http_parser.add_argument('port', type=int, nargs='?', help='Specify port for HTTP server')
    
    # Add other modules
    subparsers.add_parser('linpeas', help='Linpeas module')
    subparsers.add_parser('winpeas', help='Winpeas module')
    subparsers.add_parser('pspy', help='Pspy module')

    args = parser.parse_args()

    config = load_config()

    if args.module == 'http':
        http_directory = config['http_directory']
        
        # Create symlink for the current directory in the http_directory
        create_symlink(http_directory)
        
        # If port is provided, override default port
        http_port = args.port if args.port else config['http_port']
        
        # Start http.server
        start_http_server(http_directory, http_port)
    else:
        # Handle other tools here as needed
        print(f"Selected tool: {args.module}")


if __name__ == '__main__':
    main()
