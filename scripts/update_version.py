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