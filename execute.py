import subprocess

def run_build_client():
    subprocess.run(
        "npm run build",
        shell=True,
        cwd='./client_side'
    )
    
def run_server():
    subprocess.run(
        "python main.py",
        shell=True,
        cwd='./server_side'
    )

if __name__ == '__main__':
    run_build_client()
    run_server()