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

from setuptools import setup, find_packages  
import os  
  
# Read version from __version__.py  
version_file = os.path.join(os.path.dirname(__file__), 'casbin_cli', '__version__.py')  
if os.path.exists(version_file):  
    exec(open(version_file).read())  
    version = __version__  
else:  
    version = "1.0.0"  
  
setup(  
    name="casbin-python-cli",  
    version=version,  
    description="A command-line tool for PyCasbin",  
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    packages=find_packages(),  
    install_requires=[  
        "casbin>=1.17.0",  
    ],  
    entry_points={  
        'console_scripts': [  
            'casbin-cli=casbin_cli.client:main',  
        ],  
    },  
    python_requires='>=3.6',  
)