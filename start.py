import subprocess
import os

def start_tailscaled():
    # Start tailscaled in the background
    process = subprocess.Popen(
        ['sudo', '/usr/local/bin/tailscaled', '--tun=userspace-networking', '--socks5-server=localhost:1055'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setpgrp  # Ensure the process group is set so it continues running after the script exits
    )
    return process

def main():
    # Start tailscaled
    start_tailscaled()
    print("Tailscaled started in the background.")

if __name__ == "__main__":
    main()
