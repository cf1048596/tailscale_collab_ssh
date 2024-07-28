import subprocess
import os
import argparse
import sys

def install_dotenv():
    try:
        import dotenv
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'python-dotenv'])
        import dotenv

def install_tailscale():
    # Install Tailscale using curl and shell script
    subprocess.run('curl -fsSL https://tailscale.com/install.sh | sh', shell=True, check=True)
    print("Tailscale installed.")

def create_user():
    # Read username and password from environment variables
    username = os.getenv('NEW_USER', 'christian')
    password = os.getenv('NEW_USER_PASSWORD', 'asdf123')

    # Create a new user with the specified username and password
    subprocess.run(['sudo', 'useradd', '-m', '-s', '/bin/bash', username], check=True)
    subprocess.run(['sudo', 'chpasswd'], input=f'{username}:{password}', text=True, check=True)
    # Add the user to the sudo group
    subprocess.run(['sudo', 'usermod', '-aG', 'sudo', username], check=True)
    print(f"New user '{username}' created with the specified password and added to sudo group.")

def start_tailscaled():
    # Read additional tailscale arguments from environment variable
    tailscale_args = os.getenv('TAILSCALE_ARGS', '--tun=userspace-networking --socks5-server=localhost:1055')
    
    # Start tailscaled in the background with the specified arguments
    process = subprocess.Popen(
        ['sudo', '/usr/local/bin/tailscaled'] + tailscale_args.split(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setpgrp  # Ensure the process group is set so it continues running after the script exits
    )
    print("Tailscaled started in the background.")
    return process

def main():
    # Install dotenv if not available
    install_dotenv()

    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()

    parser = argparse.ArgumentParser(description="Manage Tailscale installation and service.")
    parser.add_argument('action', choices=['install', 'up'], nargs='?', default='install',
                        help="Specify the action to perform: 'install' to install Tailscale and create a user, 'up' to start tailscaled.")

    args = parser.parse_args()

    if args.action == 'install':
        install_tailscale()
        create_user()
    elif args.action == 'up':
        start_tailscaled()

if __name__ == "__main__":
    main()
