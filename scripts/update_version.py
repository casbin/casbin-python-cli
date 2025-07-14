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

import sys  
import re  
import os  
  
def update_version(new_version):  
    """Update version in all relevant files"""  
      
    # Update setup.py  
    setup_py_path = "setup.py"  
    with open(setup_py_path, 'r') as f:  
        content = f.read()  
      
    # Update client.py version display  
    client_py_path = "casbin_cli/client.py"  
    with open(client_py_path, 'r') as f:  
        content = f.read()  
      
    # Create __version__.py  
    version_py_path = "casbin_cli/__version__.py"  
    with open(version_py_path, 'w') as f:  
        f.write(f'__version__ = "{new_version}"\n')  
      
    print(f"Updated version to {new_version}")  
  
if __name__ == "__main__":  
    if len(sys.argv) != 2:  
        print("Usage: python update_version.py <version>")  
        sys.exit(1)  
      
    new_version = sys.argv[1]  
    update_version(new_version)