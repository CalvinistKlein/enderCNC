import os, subprocess
exe = os.readlink("/proc/72660/exe")
print("Orca exe:", exe)
out = subprocess.check_output(["strings", exe], text=True, errors="ignore")
for line in out.splitlines():
    if "remote_api" in line.lower() or "10999" in line or "13130" in line:
        print("  ", line.strip())
