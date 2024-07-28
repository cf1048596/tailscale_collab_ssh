import subprocess
import os
import argparse

def install_tailscale():
    # Install Tailscale using curl and shell script
    subprocess.run('curl -fsSL https://tailscale.com/install.sh | sh', shell=True, check=True)
    print("Tailscale installed.")

def create_user():
    # Create a new user named 'christian' with password 'asdf123'
    subprocess.run(['sudo', 'useradd', '-m', '-s', '/bin/bash', 'christian'], check=True)
    subprocess.run(['sudo', 'chpasswd'], input='christian:asdf123', text=True, check=True)
    # Add the user to the sudo group
    subprocess.run(['sudo', 'usermod', '-aG', 'sudo', 'christian'], check=True)
    print("New user 'christian' created with password 'asdf123' and added to sudo group.")

def start_tailscaled():
    # Start tailscaled in the background
    process = subprocess.Popen(
        ['sudo', '/usr/sbin/tailscaled', '--tun=userspace-networking', '--socks5-server=localhost:1055'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setpgrp  # Ensure the process group is set so it continues running after the script exits
    )
    print("Tailscaled started in the background.")
    return process

def main():
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
