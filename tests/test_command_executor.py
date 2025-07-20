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
from unittest.mock import MagicMock  
  
# Add the project root to the path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  
  
from casbin_cli.command_executor import CommandExecutor  
  
class TestCommandExecutor:  
    """Detailed test cases for CommandExecutor class"""  
      
    def test_method_name_mapping_comprehensive(self):  
        """Test comprehensive method name mapping from Java to Python style"""  
        test_mappings = [  
            ('enforceEx', 'enforce_ex'),  
            ('getAllSubjects', 'get_all_subjects'),  
            ('addPolicy', 'add_policy'),  
            ('getRolesForUser', 'get_roles_for_user'),  
            ('batchEnforce', 'batch_enforce')  
        ]  
          
        for java_name, python_name in test_mappings:  
            mock_enforcer = MagicMock()  
            setattr(mock_enforcer, python_name, MagicMock(return_value=True))  
              
            executor = CommandExecutor(mock_enforcer, java_name, ["test"])  
            executor.execute()  
              
            # Verify the Python method was called  
            getattr(mock_enforcer, python_name).assert_called_once()  
  
    def test_argument_conversion(self):  
        """Test argument type conversion"""  
        mock_enforcer = MagicMock()  
        mock_enforcer.enforce.return_value = True  
          
        executor = CommandExecutor(mock_enforcer, "enforce", ["alice", "data1", "read"])  
        result = executor.execute()  
          
        response = json.loads(result)  
        assert response["allow"] is True  
        mock_enforcer.enforce.assert_called_once_with("alice", "data1", "read")  
  
    def test_tuple_response_handling(self):  
        """Test handling of tuple responses from enforce_ex"""  
        mock_enforcer = MagicMock()  
        mock_enforcer.enforce_ex.return_value = (True, ["alice", "data1", "read"])  
          
        executor = CommandExecutor(mock_enforcer, "enforceEx", ["alice", "data1", "read"])  
        result = executor.execute()  
          
        response = json.loads(result)  
        assert response["allow"] is True  
        assert response["explain"] == ["alice", "data1", "read"]  
  
    def test_list_response_handling(self):  
        """Test handling of list responses"""  
        mock_enforcer = MagicMock()  
        mock_enforcer.get_all_subjects.return_value = ["alice", "bob", "data2_admin"]  
          
        executor = CommandExecutor(mock_enforcer, "getAllSubjects", [])  
        result = executor.execute()  
          
        response = json.loads(result)  
        assert response["allow"] is None  
        assert response["explain"] == ["alice", "bob", "data2_admin"]  
  
    def test_boolean_response_handling(self):  
        """Test handling of boolean responses"""  
        mock_enforcer = MagicMock()  
        mock_enforcer.has_policy.return_value = True  
          
        executor = CommandExecutor(mock_enforcer, "hasPolicy", ["alice", "data1", "read"])  
        result = executor.execute()  
          
        response = json.loads(result)  
        assert response["allow"] is True  
        assert response["explain"] is None  
  
    def test_error_handling(self):  
        """Test error handling for unknown methods"""  
        mock_enforcer = MagicMock()  
        del mock_enforcer.unknownMethod

        executor = CommandExecutor(mock_enforcer, "unknownMethod", ["test"])  
          
        with pytest.raises(Exception, match="Error executing command 'unknownMethod'"):  
            executor.execute()  
  
    def test_parameter_conversion_edge_cases(self):  
        """Test parameter conversion for edge cases"""  
        mock_enforcer = MagicMock()  
        mock_enforcer.get_filtered_policy.return_value = [["alice", "data1", "read"]]  
          
        # Test with integer parameter  
        executor = CommandExecutor(mock_enforcer, "getFilteredPolicy", ["0", "alice"])  
        result = executor.execute()  
          
        response = json.loads(result)  
        assert response["allow"] is None  
        assert isinstance(response["explain"], list)  
  
    def test_batch_operations(self):  
        """Test batch operation parameter handling"""  
        mock_enforcer = MagicMock()  
        mock_enforcer.add_policies = MagicMock(return_value=True)  
          
        executor = CommandExecutor(mock_enforcer, "addPolicies", ["alice,data1,read", "bob,data2,write"])  
        result = executor.execute()  
          
        response = json.loads(result)  
        assert response["allow"] is True  
        assert response["explain"] is None  
  
    def test_named_operations(self):  
        """Test named policy operations"""  
        mock_enforcer = MagicMock()  
        mock_enforcer.get_named_policy.return_value = [["alice", "data1", "read"]]  
          
        executor = CommandExecutor(mock_enforcer, "getNamedPolicy", ["p"])  
        result = executor.execute()  
          
        response = json.loads(result)  
        assert response["allow"] is None  
        assert isinstance(response["explain"], list)  
  
    def test_rbac_operations(self):  
        """Test RBAC specific operations"""  
        mock_enforcer = MagicMock()  
        mock_enforcer.get_roles_for_user.return_value = ["data2_admin"]  
          
        executor = CommandExecutor(mock_enforcer, "getRolesForUser", ["alice"])  
        result = executor.execute()  
          
        response = json.loads(result)  
        assert response["allow"] is None  
        assert response["explain"] == ["data2_admin"]