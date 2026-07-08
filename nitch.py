import subprocess
import os
import platform
import argparse
import re
from datetime import datetime

def get_sys_age():
    try:
        if platform.system() == "Darwin":
            path = '/var/db/.AppleSetupDone' if os.path.exists('/var/db/.AppleSetupDone') else '/'
        else:
            path = '/'
        birth_ts = os.path.getmtime(path)
        diff = datetime.now() - datetime.fromtimestamp(birth_ts)
        days = diff.days
        hours = diff.seconds // 3600
        if hours == 0:
            return f"{days} days"
        return f"{days} days, {hours} hours"
    except:
        return "Unknown"

def get_pkg_count():
    managers = [
        ('brew', 'echo $(($(brew list --formula 2>/dev/null | wc -l) + $(brew list --cask 2>/dev/null | wc -l)))'),
        ('port', 'port installed 2>/dev/null | wc -l'),
        ('qlist', 'qlist -I | wc -l'),
        ('emerge', 'ls -d /var/db/pkg/*/* | wc -l'),
        ('rpm', 'rpm -qa | wc -l'),
        ('pacman', 'pacman -Q | wc -l'),
        ('dpkg', 'dpkg-query -f ".\n" -W | wc -l'),
        ('dnf', 'dnf list installed | wc -l'),
        ('apt', 'apt list --installed 2>/dev/null | wc -l'),
        ('zypper', 'zypper se --installed-only | wc -l'),
        ('xbps-query', 'xbps-query -l | wc -l'),
        ('apk', 'apk info | wc -l'),
        ('nix-env', 'nix-store -q --references /run/current-system/sw 2>/dev/null | wc -l'),
    ]

    for cmd, count_cmd in managers:
        if subprocess.run(['which', cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            try:
                count = subprocess.check_output(count_cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()
                if not count or count == "0":
                    continue
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


def load_logo(logo_name, colors):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ascii_path = os.path.join(script_dir, "ascii-nitch", f"{logo_name}.txt")
        with open(ascii_path, "r") as f:
            template = f.read()
        return template.format(**colors)
    except Exception:
        return ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ascii', help='path to custom ascii file')
    args = parser.parse_args()

    blue    = "\033[38;2;122;162;247m"
    purple  = "\033[38;2;187;154;247m"
    cyan    = "\033[38;2;125;207;255m"
    green   = "\033[38;2;158;206;106m"
    magenta = "\033[38;2;255;117;127m"
    yellow  = "\033[38;2;224;175;104m"
    orange  = "\033[38;2;255;158;100m"
    red     = "\033[38;2;247;118;142m"
    white   = "\033[37m"
    reset   = "\033[0m"

    if platform.system() not in ["Linux", "Darwin"]:
        print("This fetcher only works on GNU/Linux and macOS, sorry")
        import sys; sys.exit()

    colors = {
        'blue': blue,
        'purple': purple,
        'cyan': cyan,
        'green': green,
        'magenta': magenta,
        'yellow': yellow,
        'orange': orange,
        'red': red,
        'white': white,
        'reset': reset
    }

    distro_id = ""
    distro_like = ""

    if platform.system() == "Linux":
        try:
            with open('/etc/os-release') as f:
                content = f.read()
            for line in content.splitlines():
                if line.startswith('ID='):
                    distro_id = line.split('=')[1].strip('"').lower()
                if line.startswith('ID_LIKE='):
                    distro_like = line.split('=')[1].strip('"').lower()
        except:
            pass
    elif platform.system() == "Darwin":
        distro_id = "macos"

    logo = None
    if args.ascii:
        try:
            with open(args.ascii) as f:
                logo = f.read()
        except:
            pass
    else:
        logo_keys = ['gentoo', 'arch', 'fedora', 'debian', 'ubuntu', 'macos', 'nixos']
        for key in logo_keys:
            if key in distro_id or key in distro_like:
                logo = load_logo(key, colors)
                break
        if not logo:
            logo = load_logo('linux', colors)

    # logo = logo.rstrip('\n')
    # logo_lines = logo.splitlines()
    # max_logo_width = max(visible_width(line) for line in logo_lines) if logo_lines else 0
    # offset = max_logo_width + 4

    # Print logo
    print(logo)

    # Gather info first
    username = subprocess.check_output("whoami", shell=True).decode().strip()
    hostname = subprocess.check_output("uname -n", shell=True).decode().strip()

    if platform.system() == "Darwin":
        try:
            name = subprocess.check_output("sw_vers -productName", shell=True).decode().strip()
            ver = subprocess.check_output("sw_vers -productVersion", shell=True).decode().strip()
            os_name = f"{name} {ver}"
        except:
            os_name = "macOS"
    else:
        try:
            os_name = subprocess.check_output("grep '^NAME' /etc/os-release", shell=True).decode().strip().split('=')[1].replace('"', '')
        except:
            os_name = "Linux"

    pkg_count = get_pkg_count()
    shell = os.path.basename(subprocess.check_output("echo $SHELL", shell=True).decode().strip())
    term = os.environ.get('TERM', 'unknown')

    if platform.system() == "Darwin":
        wm = "Aqua"
        try:
            if subprocess.run(['pgrep', '-x', 'yabai'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                wm = "yabai"
            elif subprocess.run(['pgrep', '-x', 'aerospace'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                wm = "AeroSpace"
            elif subprocess.run(['pgrep', '-x', 'AeroSpace'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                wm = "AeroSpace"
        except:
            pass
    else:
        wm = (
            os.environ.get('XDG_CURRENT_DESKTOP') or
            os.environ.get('DESKTOP_SESSION') or
            os.environ.get('WAYLAND_DISPLAY') and 'wayland' or
            os.environ.get('DISPLAY') and 'x11' or
            'TTY'
        )

    if platform.system() == "Darwin":
        cpu = "Apple Silicon"
        try:
            out = subprocess.check_output("system_profiler SPHardwareDataType 2>/dev/null", shell=True).decode()
            for line in out.splitlines():
                if "Chip:" in line:
                    cpu = line.split("Chip:")[1].strip()
                    break
        except:
            pass
    else:
        try:
            cpu = subprocess.check_output("lscpu | grep 'Model name'", shell=True).decode().strip().split('TM)')[1].strip()
        except:
            cpu = "Unknown"

    def get_ram():
        if platform.system() == "Darwin":
            try:
                total_bytes = int(subprocess.check_output("sysctl -n hw.memsize", shell=True).decode().strip())
                total_gb = total_bytes / (1024**3)

                vm_stat = subprocess.check_output("vm_stat", shell=True).decode()
                page_size = 4096
                free_pages = 0
                speculative_pages = 0
                for line in vm_stat.splitlines():
                    if "page size of" in line:
                        page_size = int(re.search(r"page size of (\d+) bytes", line).group(1))
                    elif "Pages free:" in line:
                        free_pages = int(line.split(":")[1].strip().replace(".", ""))
                    elif "Pages speculative:" in line:
                        speculative_pages = int(line.split(":")[1].strip().replace(".", ""))

                unused_bytes = (free_pages + speculative_pages) * page_size
                used_bytes = total_bytes - unused_bytes
                used_gb = used_bytes / (1024**3)
                return f"{total_gb:.0f} GB", f"{used_gb:.1f} GiB"
            except Exception:
                return "Unknown", "Unknown"
        else:
            try:
                out = subprocess.check_output("free -h | awk 'NR==2 {print $2, $3}'", shell=True).decode().strip()
                total, used, = out.split()
                return total, used
            except:
                return "Unknown", "Unknown"

    total, used = get_ram()

    if platform.system() == "Darwin":
        try:
            boot_time_str = subprocess.check_output("sysctl -n kern.boottime", shell=True).decode().strip()
            sec = int(re.search(r"sec = (\d+)", boot_time_str).group(1))
            import time
            diff = time.time() - sec
            days = int(diff // 86400)
            hours = int((diff % 86400) // 3600)
            minutes = int((diff % 3600) // 60)
            parts = []
            if days > 0:
                parts.append(f"{days} days")
            if hours > 0:
                parts.append(f"{hours} hours")
            if minutes > 0:
                parts.append(f"{minutes} mins")
            uptime = "up " + ", ".join(parts) if parts else "just booted"
        except:
            uptime = "Unknown"
    else:
        try:
            # Try procps uptime -p first, silence stderr if it throws an error
            uptime = subprocess.check_output("uptime -p", shell=True, stderr=subprocess.DEVNULL).decode().strip()
        except:
            try:
                # Coreutils fallback
                raw_uptime = subprocess.check_output("uptime", shell=True).decode().strip()
                if 'up' in raw_uptime:
                    uptime_str = raw_uptime.split('up', 1)[1]
                    if 'user' in uptime_str:
                        uptime_str = ','.join(uptime_str.split('user')[0].split(',')[:-1]).strip()
                    else:
                        uptime_str = uptime_str.split('load')[0].strip().rstrip(',')
                    uptime = "up " + uptime_str
                else:
                    uptime = "Unknown"
            except:
                uptime = "Unknown"

    age = get_sys_age()

    with open("/sys/class/power_supply/BAT0/capacity") as f:
        bat = int(f.read().strip()) 
    with open("/sys/class/power_supply/BAT0/status") as f:
        status = f.read().strip()

    # Build info lines
    info_lines = [
        f"{orange}{username}{white}@{green}{hostname}{reset}",
        "====================",
        f"{blue}OS:{reset} {os_name}",
        f"{cyan}Packages:{reset} {pkg_count}",
        f"{blue}Shell:{reset} {shell}",
        f"{purple}Terminal:{reset} {term}",
        f"{blue}WM:{reset} {wm}",
        f"{green}CPU:{reset} {cpu}",
        f"{purple}RAM:{reset} {used} / {total}",
        f"{blue}Uptime:{reset} {uptime}",
        f"{yellow}Age:{reset} {age}",
        f"{purple}Bat:{reset} {bat}% {red}{status}{reset}",
    ]

    # Move cursor up to align with top of logo, then print info beside it
    # print(f"\033[{len(logo_lines)}A", end="")

    # for i, line in enumerate(info_lines):
    #    print(f"\033[{offset}G {line}")

    # Pad/move down if logo is taller than info block
    #diff_lines = len(logo_lines) - len(info_lines)
    #if diff_lines > 0:
     #    print(f"\033[{diff_lines}B", end="")

    rows = [
        ("󰻀 OS", os_name, blue),
        (" hname", hostname, green),
        (" User", username, orange),
        ("󰏖 Pkgs", pkg_count, cyan),
        (" Shell", shell, blue),
        (" Terminal", term, purple),
        (" WM", wm, blue),
        ("󰍛 CPU", cpu, green),
        (" RAM", f"{used} / {total}", purple),
        (" Uptime", uptime, blue),
        ("󰃭 Age", age, yellow),
        ("󰂀 Battery", f"{bat}% {status}", purple)
    ]
    pad_x = 4
    label_width = max(len(label) for label, _, _ in rows)
    box_width = label_width + (pad_x * 2)

    print(f"{white}╭{'─' * box_width}╮{reset}")
    for label, value, color in rows:
        left_pad = pad_x
        right_pad = box_width - len(label) - pad_x
        print(f"{white}│{reset}{' ' * left_pad}{color}{label}{reset}{' ' * right_pad}{white}│{reset}  {value}")
    print(f"{white}╰{'─' * box_width}╯{reset}")

    print()

if __name__ == "__main__":
    main()

