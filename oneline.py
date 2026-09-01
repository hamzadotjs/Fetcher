import subprocess, os, platform
from datetime import datetime

def get_sys_age():
    try:
        path = '/var/db/.AppleSetupDone' if platform.system() == "Darwin" and os.path.exists('/var/db/.AppleSetupDone') else '/'
        diff = datetime.now() - datetime.fromtimestamp(os.path.getmtime(path))
        return f"{diff.days} days"
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

def main():
    if platform.system() == "Darwin":
        os_name = subprocess.check_output("sw_vers -productName", shell=True).decode().strip()
    else:
        try:
            os_name = subprocess.check_output("grep '^NAME' /etc/os-release", shell=True).decode().strip().split('=')[1].replace('"', '')
        except:
            os_name = "Linux"

    kernel = platform.release()
    pkg = get_pkg_count()
    shell = os.path.basename(os.environ.get('SHELL', '?'))
    term = os.environ.get('TERM', 'unknown')
    wm = os.environ.get('XDG_CURRENT_DESKTOP') or os.environ.get('DESKTOP_SESSION') or 'TTY'

    try:
        cpu = subprocess.check_output("lscpu | grep 'Model name'", shell=True).decode().strip().split(':')[1].strip()
        cpu = cpu.split(' CPU')[0]
    except:
        cpu = "Unknown"

    try:
        out = subprocess.check_output("free -g | awk 'NR==2 {print $3, $2}'", shell=True).decode().strip()
        used, total = out.split()
    except:
        used, total = "?", "?"

    try:
        raw = subprocess.check_output("uptime -p", shell=True, stderr=subprocess.DEVNULL).decode().strip()
        uptime = raw.replace("up ", "")
    except:
        uptime = "Unknown"

    age = get_sys_age()

    try:
        with open("/sys/class/power_supply/BAT0/capacity") as f:
            bat = f.read().strip()
    except:
        bat = "?"

    print(f"{os_name} kernel {kernel} {pkg} packages {shell} shell {term} term {wm} wm {cpu} {used}/{total}GB Ram {uptime} uptime Age {age} {bat}% battery")

if __name__ == "__main__":
    main()
