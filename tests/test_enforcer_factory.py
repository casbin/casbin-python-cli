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
import sys  
import os  
  
# Add the project root to the path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  
  
from casbin_cli.enforcer_factory import EnforcerFactory  
  
class TestEnforcerFactory:  
    """Test cases for EnforcerFactory class"""  
      
    def test_file_detection(self, temp_model_file, temp_policy_file):  
        """Test detection of file vs string input"""  
        # Test with file paths  
        enforcer = EnforcerFactory.create_enforcer(temp_model_file, temp_policy_file)  
        assert enforcer is not None  
          
        # Test basic enforcement  
        result = enforcer.enforce("alice", "data1", "read")  
        assert result is True  
  
    def test_string_detection(self):  
        """Test detection of string content input"""  
        model_content = """[request_definition]  
r = sub, obj, act  
  
[policy_definition]  
p = sub, obj, act  
  
[policy_effect]  
e = some(where (p.eft == allow))  
  
[matchers]  
m = r.sub == p.sub && r.obj == p.obj && r.act == p.act"""  
          
        policy_content = """p, alice, data1, read  
p, bob, data2, write"""  
          
        enforcer = EnforcerFactory.create_enforcer(model_content, policy_content)  
        assert enforcer is not None  
          
        # Test basic enforcement  
        result = enforcer.enforce("alice", "data1", "read")  
        assert result is True  
  
    def test_create_enforcer_with_strings(self):  
        """Test enforcer creation with string content - comprehensive test"""  
        model_text = """[request_definition]  
r = sub, obj, act  
  
[policy_definition]  
p = sub, obj, act  
  
[role_definition]  
g = _, _  
  
[policy_effect]  
e = some(where (p.eft == allow))  
  
[matchers]  
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act"""  
          
        policy_text = """p, alice, data1, read  
p, bob, data2, write  
p, data2_admin, data2, read  
p, data2_admin, data2, write  
g, alice, data2_admin"""  
          
        enforcer = EnforcerFactory.create_enforcer(model_text, policy_text)  
        assert enforcer is not None  
          
        # Test RBAC enforcement  
        assert enforcer.enforce("alice", "data1", "read") is True  
        assert enforcer.enforce("alice", "data2", "read") is True  
        assert enforcer.enforce("bob", "data1", "read") is False  
  
    def test_invalid_model_content(self):  
        """Test error handling for invalid model content"""  
        invalid_model = "invalid model content"  
        policy_content = "p, alice, data1, read"  
          
        with pytest.raises(Exception):  
            EnforcerFactory.create_enforcer(invalid_model, policy_content)  
  
    def test_invalid_policy_content(self):  
        """Test error handling for invalid policy content"""  
        model_content = """[request_definition]  
r = sub, obj, act  
  
[policy_definition]  
p = sub, obj, act  
  
[policy_effect]  
e = some(where (p.eft == allow))  
  
[matchers]  
m = r.sub == p.sub && r.obj == p.obj && r.act == p.act"""  
          
        invalid_policy = "invalid policy content"  
          
        with pytest.raises(Exception):  
            EnforcerFactory.create_enforcer(model_content, invalid_policy)  
  
    def test_empty_policy_content(self):  
        """Test handling of empty policy content"""  
        model_content = """[request_definition]  
r = sub, obj, act  
  
[policy_definition]  
p = sub, obj, act  
  
[policy_effect]  
e = some(where (p.eft == allow))  
  
[matchers]  
m = r.sub == p.sub && r.obj == p.obj && r.act == p.act"""  
          
        empty_policy = ""  
          
        enforcer = EnforcerFactory.create_enforcer(model_content, empty_policy)  
        assert enforcer is not None  
          
        # With empty policy, all requests should be denied  
        assert enforcer.enforce("alice", "data1", "read") is False  
  
    def test_mixed_file_and_string_input(self, temp_model_file):  
        """Test mixed input types - file for model, string for policy"""  
        policy_content = """p, alice, data1, read  
p, bob, data2, write"""  
          
        enforcer = EnforcerFactory.create_enforcer(temp_model_file, policy_content)  
        assert enforcer is not None  
          
        # Test enforcement  
        assert enforcer.enforce("alice", "data1", "read") is True  
        assert enforcer.enforce("bob", "data2", "write") is True  
        assert enforcer.enforce("alice", "data2", "write") is False  
  
    def test_abac_model_creation(self):  
        """Test creation of ABAC model enforcer"""  
        abac_model = """[request_definition]  
r = sub, dom, obj, act  
  
[policy_definition]  
p = sub, dom, obj, act  
  
[policy_effect]  
e = some(where (p.eft == allow))  
  
[matchers]  
m = r.sub == p.sub && r.dom == p.dom && r.obj == p.obj && r.act == p.act"""  
          
        abac_policy = """p, alice, domain1, data1, read  
p, bob, domain2, data2, write"""  
          
        enforcer = EnforcerFactory.create_enforcer(abac_model, abac_policy)  
        assert enforcer is not None  
          
        # Test ABAC enforcement  
        assert enforcer.enforce("alice", "domain1", "data1", "read") is True  
        assert enforcer.enforce("alice", "domain2", "data1", "read") is False  
        assert enforcer.enforce("bob", "domain2", "data2", "write") is True