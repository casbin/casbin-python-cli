# Copyright 2025 The casbin Authors. All Rights Reserved.  
#  
# Licensed under the Apache License, Version 2.0 (the "License");  
# you may not use this file except in compliance with the License.  
# You may obtain a copy of the License at  
#  
#      http://www.apache.org/licenses/LICENSE-2.0  
#  
# Unless required by applicable law or agreed to in writing, software  
# distributed under the License is distributed on an "AS IS" BASIS,  
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
# See the License for the specific language governing permissions and  
# limitations under the License.  
  
import os    
import sys    
import subprocess    
import platform  
import argparse  
    
def build_binary():    
    """Build standalone binary using PyInstaller"""  
      
    # Parse command line arguments  
    parser = argparse.ArgumentParser()  
    parser.add_argument('--platform', help='Target platform (linux, darwin, windows)')  
    args = parser.parse_args()  
      
    # Install PyInstaller if not present    
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)    
      
    # Get platform and architecture info  
    system = platform.system().lower()  
    arch = platform.machine().lower()  
        
    arch_mapping = {  
        'x86_64': 'x86_64',  
        'amd64': 'x86_64',   
        'arm64': 'arm64',  
        'aarch64': 'arm64',  
        'i386': '386',  
        'i686': '386'  
    }  
      
    normalized_arch = arch_mapping.get(arch, arch)  
       
    if args.platform:  
        target_platform = args.platform  
    else:  
        # Fallback to auto-detection  
        if system == 'darwin':  
            target_platform = 'darwin'  
        elif system == 'linux':  
            target_platform = 'linux'  
        elif system == 'windows':  
            target_platform = 'windows'  
        else:  
            target_platform = system  
      
    # Build binary name  
    binary_name = f"casbin-python-cli-{target_platform}-{normalized_arch}"  
    executable_name = binary_name  
    if target_platform == "windows":    
        executable_name += ".exe"  
        
    cmd = [    
        "pyinstaller",    
        "--onefile",    
        "--name", binary_name,
        "--console",    
        "--paths", ".",    
        "--hidden-import", "casbin_cli",    
        "--hidden-import", "casbin",    
        "--hidden-import", "casbin_cli.client",    
        "--hidden-import", "casbin_cli.command_executor",     
        "--hidden-import", "casbin_cli.enforcer_factory",    
        "--hidden-import", "casbin_cli.response",    
        "--hidden-import", "casbin_cli.utils",    
        "--collect-all", "casbin",   
        "casbin_cli/client.py"    
    ]   
        
    subprocess.run(cmd, check=True)    
        
    print(f"Binary built successfully: dist/{executable_name}")    
    
if __name__ == "__main__":    
    build_binary()