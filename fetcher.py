import subprocess
import os
import platform
import argparse

with open('/etc/os-release') as f:
    content = f.read()

parser = argparse.ArgumentParser()
parser.add_argument('--ascii', help='path to custom ascii file')
args = parser.parse_args()

blue    = "\033[38;2;122;162;247m"
purple  = "\033[38;2;187;154;247m"
cyan    = "\033[38;2;125;207;255m"
green   = "\033[38;2;158;206;106m"
reset   = "\033[0m"

if platform.system() != "Linux":
    print("this fetcher only works on linux, sorry")
    exit()

tux = r"""
    .--.
   |o_o |
   |:_/ |
  //   \ \
 (|     | )
/'\_   _/`\
\___)=(___/
"""

Arch = r"""
    /\
   /  \
  /\   \
 /  __  \
/__/  \__\
"""

if args.ascii:
    with open(args.ascii) as f:
        logo = f.read()
elif 'ID=arch' in content or 'ID_LIKE=arch' in content:
    logo = Arch
else:
    logo = tux

logo_lines = logo.splitlines()
max_logo_width = max(len(line) for line in logo_lines) if logo_lines else 0
offset = max_logo_width + 4

print(logo)
print(f"\033[{len(logo_lines)}A", end="")

os_name = subprocess.check_output("grep '^NAME' /etc/os-release", shell=True).decode().strip().split('=')[1].strip('"')
print(f"\033[{offset}G {blue}OS:{reset} {os_name}") 

pkg_count = subprocess.check_output("pacman -Q | wc -l", shell=True).decode().strip()
print(f"\033[{offset}G {cyan}Packages:{reset} {pkg_count}")

shell = os.path.basename(subprocess.check_output("echo $SHELL", shell=True).decode().strip())
print(f"\033[{offset}G {blue}Shell:{reset} {shell}")

term = os.environ.get('TERM', 'unknown')
print(f"\033[{offset}G {purple}Terminal:{reset} {term}")

wm = (
    os.environ.get('XDG_CURRENT_DESKTOP') or
    os.environ.get('DESKTOP_SESSION') or
    os.environ.get('WAYLAND_DISPLAY') and 'wayland' or
    os.environ.get('DISPLAY') and 'x11' or
    'unknown'
)
print(f"\033[{offset}G {blue}WM:{reset} {wm}")

cpu = subprocess.check_output("lscpu | grep 'Model name'", shell=True).decode().strip().split(':')[1].strip()
print(f"\033[{offset}G {green}CPU:{reset} {cpu}")

def get_ram():
    out = subprocess.check_output("free -h | awk 'NR==2 {print $2, $3}'", shell=True).decode().strip()
    total, used, = out.split()
    return total, used

total, used = get_ram()
print(f"\033[{offset}G {purple}RAM:{reset} {used} / {total}")

uptime = subprocess.check_output("uptime -p", shell=True).decode().strip()
print(f"\033[{offset}G {blue}Uptime:{reset} {uptime}")

print(f"\033[{len(logo_lines)}B")
