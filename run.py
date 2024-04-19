import subprocess

def run_scripts(script_names):
    for script_name in script_names:
        print(f"Running {script_name}...")
        subprocess.run(["python", script_name], check=True)

scripts = ['ivy_server.py', 'ivy_updater.py']

run_scripts(scripts)
