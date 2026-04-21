import subprocess
import os
import platform
import argparse
import re

## Measurement
def visible_width(s):
    return len(re.sub(r'\033\[[0-9;]*m', '', s))

def get_os_info():
    info = {}
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release') as f:
                for line in f:
                    if '=' in line:
                        parts = line.rstrip().split('=', 1)
                        if len(parts) == 2:
                            key, value = parts
                            info[key] = value.strip('"')
    except Exception:
        pass
    return info

os_info = get_os_info()
distro_id = os_info.get('ID', 'linux').lower()
distro_like = os_info.get('ID_LIKE', '').lower()

parser = argparse.ArgumentParser()
parser.add_argument('--ascii', help='path to custom ascii file')
args = parser.parse_args()

# Colors
blue    = "\033[38;2;122;162;247m"
purple  = "\033[38;2;187;154;247m"
cyan    = "\033[38;2;125;207;255m"
green   = "\033[38;2;158;206;106m"
magenta = "\033[38;2;255;117;127m"
yellow  = "\033[38;2;224;175;104m"
reset   = "\033[0m"

if platform.system() != "Linux":
    print("This fetcher only works on Linux, sorry.")
    exit()

tux = f"""{green}
    .--.
   |o_o |
   |:_/ |
  //   \\ \\
 (|     | )
/'\\_   _/`\\
\\___)=(___/
{reset}"""

arch_logo = f"""{cyan}
      /\\
     /  \\
    /\\   \\
   /      \\
  /   __   \\
 /__ /  \\ __\\
{reset}"""

fedora_logo = f"""{blue}
           _nnnn_
          dGGGGMMb
         @p~qp~~qMb
         M|@||@) M|
         @,----.@@
        f`^^^^-'f\\
       p`vvvvv'p  \\
      /           \\
{reset}"""

debian_logo = f"""{magenta}
       _____
      /  __ \\
     |  /    |
     |  \\___-
      \\_
{reset}"""

ubuntu_logo = f"""{yellow}
         _ 
     ---(_)---
    /  /   \\  \\
   |  |     |  |
    \\  \\   /  /
     ---(_)---
{reset}"""

logos = {
    'arch': arch_logo,
    'fedora': fedora_logo,
    'debian': debian_logo,
    'ubuntu': ubuntu_logo,
    'linux': tux
}

logo = logos.get('linux')
if args.ascii:
    try:
        with open(args.ascii) as f:
            logo = f.read()
    except Exception:
        pass
else:
    # Try to match ID or ID_LIKE
    matched = False
    for key in logos:
        if key in distro_id or key in distro_like:
            logo = logos[key]
            matched = True
            break
    if not matched:
        logo = logos.get('linux')

logo_lines = logo.strip('\n').splitlines()
max_logo_width = max(visible_width(line) for line in logo_lines) if logo_lines else 0
offset = max_logo_width + 4

# Print logo
print(logo)
# Move cursor up to the start of the logo
print(f"\033[{len(logo_lines)}A", end="")

def get_pkg_count():
    # Detect package manager - Priority order
    managers = [
        ('rpm', 'rpm -qa | wc -l'),
        ('pacman', 'pacman -Q | wc -l'),
        ('dpkg', 'dpkg-query -f ".\n" -W | wc -l'),
        ('dnf', 'dnf list installed | wc -l'),
        ('apt', 'apt list --installed 2>/dev/null | wc -l'),
        ('zypper', 'zypper se --installed-only | wc -l'),
        ('xbps-query', 'xbps-query -l | wc -l'),
        ('apk', 'apk info | wc -l')
    ]
    
    for cmd, count_cmd in managers:
        if subprocess.run(['which', cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            try:
                count = subprocess.check_output(count_cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()
                if not count or count == "0":
                    continue
                # Handle special cases for headers
                if cmd == 'dnf':
                    return str(max(0, int(count) - 1))
                if cmd == 'apt' and 'apt list' in count_cmd:
                    return str(max(0, int(count) - 1))
                return count
            except Exception:
                continue
    return "0"

def get_cpu():
    try:
        with open('/proc/cpuinfo') as f:
            for line in f:
                if 'model name' in line:
                    cpu = line.split(':', 1)[1].strip()
                    # Clean up CPU string
                    cpu = re.sub(r'\(R\)|\(TM\)|Processor|Core|CPU|@.*', '', cpu)
                    return ' '.join(cpu.split())
    except Exception:
        pass
    return "Unknown"

def get_ram():
    try:
        with open('/proc/meminfo') as f:
            meminfo = {line.split(':')[0]: line.split(':')[1].strip() for line in f}
        total = int(meminfo['MemTotal'].split()[0]) / 1024 / 1024 # GiB
        available = int(meminfo.get('MemAvailable', meminfo.get('MemFree')).split()[0]) / 1024 / 1024
        used = total - available
        return f"{used:.1f}Gi / {total:.1f}Gi"
    except Exception:
        return "Unknown"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            if hours > 0:
                return f"up {hours} hours, {minutes} minutes"
            else:
                return f"up {minutes} minutes"
    except Exception:
        return "Unknown"

# OS
print(f"\033[{offset}G {blue}OS:{reset} {os_info.get('PRETTY_NAME', 'Linux')}") 

# Packages
pkg_count = get_pkg_count()
print(f"\033[{offset}G {cyan}Packages:{reset} {pkg_count}")

# Shell
shell = os.path.basename(os.environ.get('SHELL', '/bin/sh'))
print(f"\033[{offset}G {blue}Shell:{reset} {shell}")

# Terminal
term = os.environ.get('TERM', 'unknown')
if term == 'dumb' or not term: # Common in subshells
    term = os.environ.get('TERMINAL_EMULATOR', 'xterm-256color')
print(f"\033[{offset}G {purple}Terminal:{reset} {term}")

# WM/DE
wm = (
    os.environ.get('XDG_CURRENT_DESKTOP') or
    os.environ.get('DESKTOP_SESSION') or
    os.environ.get('WAYLAND_DISPLAY') and 'wayland' or
    os.environ.get('DISPLAY') and 'x11' or
    'unknown'
)
print(f"\033[{offset}G {blue}WM:{reset} {wm}")

# CPU
print(f"\033[{offset}G {green}CPU:{reset} {get_cpu()}")

# RAM
print(f"\033[{offset}G {purple}RAM:{reset} {get_ram()}")

# Uptime
print(f"\033[{offset}G {blue}Uptime:{reset} {get_uptime()}")

# Move cursor down to the end of the logo
print(f"\033[{len(logo_lines)}B")
