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
  
import pytest  
import os  
import tempfile  
from pathlib import Path
import sys 

sys._called_from_test = True
  
@pytest.fixture  
def temp_policy_file():  
    """Create a temporary policy file for testing"""  
    content = """p, alice, data1, read  
p, bob, data2, write  
p, data2_admin, data2, read  
p, data2_admin, data2, write  
g, alice, data2_admin"""  
      
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:  
        f.write(content)  
        f.flush()   
        yield f.name  
    try:  
        os.unlink(f.name)  
    except FileNotFoundError:  
        pass 
  
@pytest.fixture  
def temp_model_file():  
    """Create a temporary model file for testing"""  
    content = """[request_definition]  
r = sub, obj, act  
  
[policy_definition]  
p = sub, obj, act  
  
[role_definition]  
g = _, _  
  
[policy_effect]  
e = some(where (p.eft == allow))  
  
[matchers]  
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act"""  
      
    with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:  
        f.write(content)
        f.flush()  
        yield f.name  
      
    try:
        os.unlink(f.name)
    except FileNotFoundError:
        pass
    
@pytest.fixture  
def basic_policy_file():  
    """Create a basic policy file for testing"""  
    content = """p, alice, data1, read  
p, alice, data1, write  
p, bob, data2, write"""  
      
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:  
        f.write(content)  
        yield f.name  
    os.unlink(f.name)  
  
@pytest.fixture  
def basic_model_file():  
    """Create a basic model file for testing"""  
    content = """[request_definition]  
r = sub, obj, act  
  
[policy_definition]  
p = sub, obj, act  
  
[policy_effect]  
e = some(where (p.eft == allow))  
  
[matchers]  
m = r.sub == p.sub && r.obj == p.obj && r.act == p.act"""  
      
    with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as f:  
        f.write(content)  
        yield f.name  
    os.unlink(f.name)