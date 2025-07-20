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
import json  
import sys  
import os  
from unittest.mock import patch, MagicMock  
  
# Add the project root to the path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  
  
from casbin_cli.client import Client  
from casbin_cli.command_executor import CommandExecutor  
from casbin_cli.enforcer_factory import EnforcerFactory  
  
class TestClient:  
    """Test cases for the main Client class, based on Java ClientTest.java"""  
      
    def test_rbac_enforcement(self, temp_model_file, temp_policy_file):  
        """Test RBAC enforcement scenarios - equivalent to Java testRBAC()"""  
        test_cases = [  
            (["alice", "data1", "read"], True),  
            (["alice", "data1", "write"], False),  
            (["alice", "data2", "read"], True),  
            (["alice", "data2", "write"], True),  
            (["bob", "data1", "read"], False),  
            (["bob", "data1", "write"], False),  
            (["bob", "data2", "read"], False),  
            (["bob", "data2", "write"], True),  
        ]  
      
        for args, expected in test_cases:  
            try:  
                result = Client.run(["enforce", "-m", temp_model_file, "-p", temp_policy_file] + args)  
                response = json.loads(result)  
                assert response["allow"] == expected  
                assert response["explain"] is None  
            except RuntimeError as e:  
                pytest.fail(f"Client.run failed with RuntimeError for args {args}: {e}")
  
    def test_enforce_ex(self, temp_model_file, temp_policy_file):  
        """Test enforceEx command - equivalent to Java testManagementApi() enforceEx"""  
        result = Client.run(["enforceEx", "-m", temp_model_file, "-p", temp_policy_file, "alice", "data1", "read"])  
        response = json.loads(result)  
        assert response["allow"] is True  
        assert isinstance(response["explain"], list)  
        assert len(response["explain"]) == 3  
  
    def test_policy_management(self, temp_model_file, temp_policy_file):  
        """Test policy add/remove operations - equivalent to Java testAddAndRemovePolicy()"""  
        # Test add policy  
        result = Client.run(["addPolicy", "-m", temp_model_file, "-p", temp_policy_file, "eve", "data3", "read"])  
        response = json.loads(result)  
        assert response["allow"] is True  
          
        # Test remove policy  
        result = Client.run(["removePolicy", "-m", temp_model_file, "-p", temp_policy_file, "eve", "data3", "read"])  
        response = json.loads(result)  
        assert response["allow"] is True  
  
    def test_data_retrieval_apis(self, temp_model_file, temp_policy_file):  
        """Test data retrieval APIs - equivalent to Java testManagementApi() data retrieval"""  
        # Test getAllSubjects  
        result = Client.run(["getAllSubjects", "-m", temp_model_file, "-p", temp_policy_file])  
        response = json.loads(result)  
        assert response["allow"] is None  
        assert isinstance(response["explain"], list)  
        assert "alice" in response["explain"]  
        assert "bob" in response["explain"]  
          
        # Test getAllObjects  
        result = Client.run(["getAllObjects", "-m", temp_model_file, "-p", temp_policy_file])  
        response = json.loads(result)  
        assert response["allow"] is None  
        assert isinstance(response["explain"], list)  
        assert "data1" in response["explain"]  
        assert "data2" in response["explain"]  
          
        # Test getAllActions  
        result = Client.run(["getAllActions", "-m", temp_model_file, "-p", temp_policy_file])  
        response = json.loads(result)  
        assert response["allow"] is None  
        assert isinstance(response["explain"], list)  
        assert "read" in response["explain"]  
        assert "write" in response["explain"]  
  
    def test_rbac_operations(self, temp_model_file, temp_policy_file):  
        """Test RBAC operations - equivalent to Java testRBACApi()"""  
        # Test getRolesForUser  
        result = Client.run(["getRolesForUser", "-m", temp_model_file, "-p", temp_policy_file, "alice"])  
        response = json.loads(result)  
        assert response["allow"] is None  
        assert isinstance(response["explain"], list)  
        assert "data2_admin" in response["explain"]  
          
        # Test getUsersForRole  
        result = Client.run(["getUsersForRole", "-m", temp_model_file, "-p", temp_policy_file, "data2_admin"])  
        response = json.loads(result)  
        assert response["allow"] is None  
        assert isinstance(response["explain"], list)  
        assert "alice" in response["explain"]  
          
        # Test hasRoleForUser  
        result = Client.run(["hasRoleForUser", "-m", temp_model_file, "-p", temp_policy_file, "alice", "data2_admin"])  
        response = json.loads(result)  
        assert response["allow"] is True  
  
    def test_grouping_policy_operations(self, temp_model_file, temp_policy_file):  
        """Test grouping policy operations"""  
        # Test getGroupingPolicy  
        result = Client.run(["getGroupingPolicy", "-m", temp_model_file, "-p", temp_policy_file])  
        response = json.loads(result)  
        assert response["allow"] is None  
        assert isinstance(response["explain"], list)  
          
        # Test addGroupingPolicy  
        result = Client.run(["addGroupingPolicy", "-m", temp_model_file, "-p", temp_policy_file, "group1", "data2_admin"])  
        response = json.loads(result)  
        assert response["allow"] is True  
          
        # Test removeGroupingPolicy  
        result = Client.run(["removeGroupingPolicy", "-m", temp_model_file, "-p", temp_policy_file, "group1", "data2_admin"])  
        response = json.loads(result)  
        assert response["allow"] is True  
  
    def test_policy_queries(self, temp_model_file, temp_policy_file):  
        """Test policy query operations"""  
        # Test getPolicy  
        result = Client.run(["getPolicy", "-m", temp_model_file, "-p", temp_policy_file])  
        response = json.loads(result)  
        assert response["allow"] is None  
        assert isinstance(response["explain"], list)  
        assert len(response["explain"]) > 0  
          
        # Test hasPolicy  
        result = Client.run(["hasPolicy", "-m", temp_model_file, "-p", temp_policy_file, "alice", "data1", "read"])  
        response = json.loads(result)  
        assert response["allow"] is True  
          
        # Test getFilteredPolicy  
        result = Client.run(["getFilteredPolicy", "-m", temp_model_file, "-p", temp_policy_file, "0", "alice"])  
        response = json.loads(result)  
        assert response["allow"] is None  
        assert isinstance(response["explain"], list)  
  
    def test_string_based_input(self):  
        """Test string-based model and policy input - equivalent to Java testParseString()"""  
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
          
        result = Client.run(["enforce", "-m", model_text, "-p", policy_text, "alice", "data1", "read"])  
        response = json.loads(result)  
        assert response["allow"] is True  
        assert response["explain"] is None  
  
    def test_error_handling(self):  
        """Test error handling for invalid inputs"""  
        with pytest.raises((RuntimeError, ValueError)):  
            Client.run(["enforce", "-m", "nonexistent.conf", "-p", "nonexistent.csv", "alice", "data1", "read"])  
  
    def test_help_and_version(self):  
        """Test help and version commands"""  
        # Test help  
        result = Client.run(["-h"])  
        assert result == ""  
          
        result = Client.run(["--help"])  
        assert result == ""  
          
        # Test version  
        with patch('builtins.print') as mock_print:  
            result = Client.run(["-v"])  
            mock_print.assert_called()  
          
        with patch('builtins.print') as mock_print:  
            result = Client.run(["--version"])  
            mock_print.assert_called()  
  
    def test_abac_enforcement(self):  
        """Test ABAC enforcement scenarios - equivalent to Java testABAC()"""  
        model_text = """[request_definition]  
r = sub, dom, obj, act  
  
[policy_definition]  
p = sub, dom, obj, act  
  
[policy_effect]  
e = some(where (p.eft == allow))  
  
[matchers]  
m = r.sub == p.sub && r.dom == p.dom && r.obj == p.obj && r.act == p.act"""  
          
        policy_text = """p, alice, domain1, data1, read  
p, alice, domain1, data1, write  
p, bob, domain2, data2, read"""  
          
        # Test cases based on Java ClientTest.java ABAC tests  
        test_cases = [  
            (["alice", "domain1", "data1", "read"], True),  
            (["alice", "domain1", "data1", "write"], True),  
            (["alice", "domain2", "data1", "read"], False),  
            (["bob", "domain2", "data2", "read"], True),  
            (["bob", "domain1", "data2", "read"], False),  
        ]  
          
        for args, expected in test_cases:  
            result = Client.run(["enforce", "-m", model_text, "-p", policy_text] + args)  
            response = json.loads(result)  
            assert response["allow"] == expected  
            assert response["explain"] is None  
  
    def test_custom_function(self):  
        """Test custom function support - equivalent to Java testCustomFunction()"""  
        # Note: Custom function testing would require implementing the -AF flag support  
        # This is a placeholder for when that functionality is added  
        pass