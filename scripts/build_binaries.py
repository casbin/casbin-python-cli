import os  
import sys  
import subprocess  
import platform  
  
def build_binary():  
    """Build standalone binary using PyInstaller"""  
      
    # Install PyInstaller if not present  
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)  
      
    # Get platform info  
    system = platform.system().lower()  
    arch = platform.machine().lower()  
      
    # Build binary  
    binary_name = f"casbin-cli-{system}-{arch}"  
    if system == "windows":  
        binary_name += ".exe"  
      
    cmd = [  
        "pyinstaller",  
        "--onefile",  
        "--name", binary_name,  
        "--console",  
        "casbin_cli/client.py"  
    ]  
      
    subprocess.run(cmd, check=True)  
      
    print(f"Binary built successfully: dist/{binary_name}")  
  
if __name__ == "__main__":  
    build_binary()