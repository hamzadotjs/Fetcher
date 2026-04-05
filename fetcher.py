import subprocess
import os
import platform


blue    = "\033[38;2;122;162;247m"  # #7aa2f7
purple  = "\033[38;2;187;154;247m"  # #bb9af7
cyan    = "\033[38;2;125;207;255m"  # #7dcfff
green   = "\033[38;2;158;206;106m"  # #9ece6a
reset   = "\033[0m"


os_name = platform.system()

if os_name != "Linux":
    print("this fetcher only works on linux, sorry")
    exit()

tux = r"""
    .--.
   |o_o |
   |:_/ |
  //   \ \\
 (|     | )
/'\_   _/`\\
\___)=(___/
"""

Arch = r"""
    /\
   /  \
  /\   \
 /  __  \
/__/  \__\

"""

with open('/etc/os-release') as f:
    content = f.read()

if 'ID=arch' in content or 'ID_LIKE=arch' in content:
    logo = Arch
else:
    logo = tux


logo_lines_padded = [line.ljust(12) for line in logo.splitlines()]
logo = '\n'.join(logo_lines_padded)
logo_lines = logo.splitlines()  # Still 5 lines
print(logo)
print(f"\033[{len(logo_lines)}A", end="")

os_name = subprocess.check_output("grep '^NAME' /etc/os-release", shell=True).decode().strip().split('=')[1].strip('"')
print(f"\033[25G {blue}OS:{reset} {os_name}") 


pkg_count = subprocess.check_output("pacman -Q | wc -l", shell=True).decode().strip()
print(f"\033[25G {cyan}Packages:{reset} {pkg_count}")


shell = os.path.basename(subprocess.check_output("echo $SHELL", shell=True).decode().strip())
print(f"\033[25G {blue}Shell:{reset} {shell}")

term = os.environ.get('TERM', 'unknown')
print(f"\033[25G {purple}Terminal:{reset} {term}")

wm = (
    os.environ.get('XDG_CURRENT_DESKTOP') or
    os.environ.get('DESKTOP_SESSION') or
    os.environ.get('WAYLAND_DISPLAY') and 'wayland' or
    os.environ.get('DISPLAY') and 'x11' or
    'unknown'
)

print(f"\033[25G {purple}WM:{reset} {wm}")

cpu = subprocess.check_output("lscpu | grep 'Model name'", shell=True).decode().strip().split(':')[1].strip()
print(f"\033[25G {green}CPU:{reset} {cpu}")



def get_ram():
    out = subprocess.check_output("free -h | awk 'NR==2 {print $2, $3}'", shell=True).decode().strip()
    total, used, = out.split()
    return total, used

total, used = get_ram()
print(f"\033[25G {purple}RAM:{reset} {used} / {total}")


uptime = subprocess.check_output("uptime -p", shell=True).decode().strip()

print(f"\033[25G {blue}Uptime:{reset} {uptime}")

