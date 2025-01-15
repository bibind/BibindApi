import subprocess


def run_playbook(playbook_path):
    cmd = f"ansible-playbook {playbook_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr