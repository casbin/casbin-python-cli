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
      
    print(f"Binary built successfully: dist/{binary_name}")  
  
if __name__ == "__main__":  
    build_binary()