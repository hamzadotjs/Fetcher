import subprocess
import os
import platform


blue    = "\033[38;2;122;162;247m"  # #7aa2f7
purple  = "\033[38;2;187;154;247m"  # #bb9af7
cyan    = "\033[38;2;125;207;255m"  # #7dcfff
green   = "\033[38;2;158;206;106m"  # #9ece6a
reset   = "\033[0m"



os_name = platform.system()

tux = r"""
    .--.
   |o_o |
   |:_/ |
  //   \ \\
 (|     | )
/'\_   _/`\\
\___)=(___/
"""

win = """
█████╗
██╔══╝ 
█████╗ 
╚════╝ 
"""

mac = r'''
                       .8 
                     .888
                   .8888'
                  .8888'
                  888'
                  8'
     .88888888888. .88888888888.
  .8888888888888888888888888888888.
.8888888888888888888888888888888888.
.&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.
`%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.
 `00000000000000000000000000000000000'
  `000000000000000000000000000000000'
   `0000000000000000000000000000000'
     `###########################'
      `#######################'
         `#########''########'
           `""""""'  `"""""'
'''
if os_name == "Linux":
    logo = tux
elif os_name == "Windows":
    logo = win
elif os_name == "Darwin":
    logo = mac

logo_lines = logo.strip().splitlines()
print(logo)
print(f"\033[{len(logo_lines)}A", end="")


os_name = subprocess.check_output("grep '^NAME' /etc/os-release", shell=True).decode().strip().split('=')[1].strip('"')
print(f"\033[25G {blue}OS:{reset} {os_name}") 

def get_ram():
    out = subprocess.check_output("free -h | awk 'NR==2 {print $2, $3}'", shell=True).decode().strip()
    total, used, = out.split()
    return total, used

total, used = get_ram()
print(f"\033[25G {purple}RAM:{reset} {used} / {total}")

pkg_count = subprocess.check_output("pacman -Q | wc -l", shell=True).decode().strip()
print(f"\033[25G {cyan}Packages:{reset} {pkg_count}")

cpu = subprocess.check_output("lscpu | grep 'Model name'", shell=True).decode().strip().split(':')[1].strip()
print(f"\033[25G {green}CPU:{reset} {cpu}")


uptime = subprocess.check_output("uptime -p", shell=True).decode().strip()

print(f"\033[25G {blue}Uptime:{reset} {uptime}")

shell = os.path.basename(subprocess.check_output("echo $SHELL", shell=True).decode().strip())
print(f"\033[25G {blue}Shell:{reset} {shell}")


wm = (
    os.environ.get('XDG_CURRENT_DESKTOP') or
    os.environ.get('DESKTOP_SESSION') or
    os.environ.get('WAYLAND_DISPLAY') and 'wayland' or
    os.environ.get('DISPLAY') and 'x11' or
    'unknown'
)

print(f"\033[25G {purple}WM:{reset} {wm}")
