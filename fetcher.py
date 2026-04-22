import subprocess
import os
import platform
import argparse
import re

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

##mesument
def visible_width(s):
    return len(re.sub(r'\033\[[0-9;]*m', '', s))

with open('/etc/os-release') as f:
    content = f.read()

parser = argparse.ArgumentParser()
parser.add_argument('--ascii', help='path to custom ascii file')
args = parser.parse_args()

blue    = "\033[38;2;122;162;247m"
purple  = "\033[38;2;187;154;247m"
cyan    = "\033[38;2;125;207;255m"
green   = "\033[38;2;158;206;106m"
magenta = "\033[38;2;255;117;127m"
yellow  = "\033[38;2;224;175;104m"
reset   = "\033[0m"

if platform.system() != "Linux":
    print("This fetcher only works on GNU/Linux, sorry")
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

fedora_logo = f""" {blue}
                                        
                                        
                      .cxO00Od:.        
                    ,0WMMMMMMMMWk'      
                   lWMMXo;'';oXWMWc     
                  .WMMX.      .XMMW.    
                  :MMMK        0MMW.    
                  cMMMK        'dx;     
                  cMMMK                 
         .':llll, cMMMXllllc.           
      .cOWMMMMMMx cMMMMMMMMMx           
     :XMMMXOdddd; cMMMNddddl.           
    cWMMK;.       cMMMK                 
   .NMMX.         cMMMK                 
   ;MMMK          cMMMO                 
   .XMMW;        .kMMMc                 
    ,XMMWx;.   .:0MMMx.                 
     .xWMMMWXXNMMMMK:                   
       .ckKWMMWX0o,                     
        '\"\"\"\"'                                        
{reset}
 """

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

with open('/etc/os-release') as f:
    content = f.read()

# We need to define these so the loop below doesn't crash
distro_id = ""
distro_like = ""

for line in content.splitlines():
    if line.startswith('ID='):
        distro_id = line.split('=')[1].strip('"').lower()
    if line.startswith('ID_LIKE='):
        distro_like = line.split('=')[1].strip('"').lower()

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

        ## logo printing logic
logo_lines = logo.splitlines()
max_logo_width = max(visible_width(line) for line in logo_lines) if logo_lines else 0
offset = max_logo_width + 4

print(logo)
print(f"\033[{len(logo_lines)}A", end="")

os_name = subprocess.check_output("grep '^NAME' /etc/os-release", shell=True).decode().strip().split('=')[1].strip('"')
print(f"\033[{offset}G {blue}OS:{reset} {os_name}") 

# pkg_count = subprocess.check_output("pacman -Q | wc -l", shell=True).decode().strip()
# print(f"\033[{offset}G {cyan}Packages:{reset} {pkg_count}")

pkg_count = get_pkg_count()
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

cpu = subprocess.check_output("lscpu | grep 'Model name'", shell=True).decode().strip().split('TM)')[1].strip()
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
