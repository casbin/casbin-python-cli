import json  
import inspect  
from typing import Any, List  
from .response import ResponseBody  
  
class CommandExecutor:  
    def __init__(self, enforcer, command_name, args):  
        """Initialize the command executor"""  
        self.enforcer = enforcer  
        self.command_name = command_name  
        self.args = args  
  
    def execute(self):  
        """Execute the command and return the result in JSON format"""  
        try:  
            # Method name mapping: Java style -> Python style 
            method_mapping = {  
                'enforceEx': 'enforce_ex',  
                'enforceExWithMatcher': 'enforce_ex_with_matcher',  
                'batchEnforce': 'batch_enforce',  
                'getAllSubjects': 'get_all_subjects',  
                'getAllObjects': 'get_all_objects',  
                'getAllActions': 'get_all_actions',  
                'getAllRoles': 'get_all_roles',  
                'getAllNamedSubjects': 'get_all_named_subjects',  
                'getAllNamedObjects': 'get_all_named_objects',  
                'getAllNamedActions': 'get_all_named_actions',  
                'getAllNamedRoles': 'get_all_named_roles',  
                'addPolicy': 'add_policy',  
                'removePolicy': 'remove_policy',  
                'updatePolicy': 'update_policy',  
                'addGroupingPolicy': 'add_grouping_policy',  
                'removeGroupingPolicy': 'remove_grouping_policy',  
                'updateGroupingPolicy': 'update_grouping_policy',  
                'addNamedPolicy': 'add_named_policy',  
                'removeNamedPolicy': 'remove_named_policy',  
                'addNamedPolicies': 'add_named_policies',  
                'removeNamedPolicies': 'remove_named_policies',  
                'addNamedGroupingPolicy': 'add_named_grouping_policy',  
                'removeNamedGroupingPolicy': 'remove_named_grouping_policy',  
                'addNamedGroupingPolicies': 'add_named_grouping_policies',  
                'removeNamedGroupingPolicies': 'remove_named_grouping_policies',  
                'removeFilteredPolicy': 'remove_filtered_policy',  
                'removeFilteredNamedPolicy': 'remove_filtered_named_policy',  
                'removeFilteredGroupingPolicy': 'remove_filtered_grouping_policy',  
                'removeFilteredNamedGroupingPolicy': 'remove_filtered_named_grouping_policy',  
                'hasPolicy': 'has_policy',  
                'hasNamedPolicy': 'has_named_policy',  
                'hasGroupingPolicy': 'has_grouping_policy',  
                'hasNamedGroupingPolicy': 'has_named_grouping_policy',  
                'getPolicy': 'get_policy',  
                'getNamedPolicy': 'get_named_policy',  
                'getGroupingPolicy': 'get_grouping_policy',  
                'getNamedGroupingPolicy': 'get_named_grouping_policy',  
                'getFilteredPolicy': 'get_filtered_policy',  
                'getFilteredNamedPolicy': 'get_filtered_named_policy',  
                'getFilteredGroupingPolicy': 'get_filtered_grouping_policy',  
                'getFilteredNamedGroupingPolicy': 'get_filtered_named_grouping_policy',  
                'getRolesForUser': 'get_roles_for_user',  
                'getUsersForRole': 'get_users_for_role',  
                'hasRoleForUser': 'has_role_for_user',  
                'addRoleForUser': 'add_role_for_user',  
                'deleteRoleForUser': 'delete_role_for_user',  
                'deleteRolesForUser': 'delete_roles_for_user',  
                'deleteUser': 'delete_user',  
                'deleteRole': 'delete_role',  
                'deletePermission': 'delete_permission',  
                'addPermissionForUser': 'add_permission_for_user',  
                'deletePermissionForUser': 'delete_permission_for_user',  
                'deletePermissionsForUser': 'delete_permissions_for_user',  
                'getPermissionsForUser': 'get_permissions_for_user',  
                'hasPermissionForUser': 'has_permission_for_user',  
                'getImplicitRolesForUser': 'get_implicit_roles_for_user',  
                'getImplicitPermissionsForUser': 'get_implicit_permissions_for_user',  
                'getImplicitUsersForRole': 'get_implicit_users_for_role',
                'addPolicies': 'add_policies',  
            }  
              
              
            actual_method_name = method_mapping.get(self.command_name, self.command_name)  
              

            if not hasattr(self.enforcer, actual_method_name):      
                available_methods = [method for method in dir(self.enforcer) if not method.startswith('_')]  
                raise AttributeError(f"Method '{actual_method_name}' not found. Available methods: {available_methods[:10]}...")  
  
            method = getattr(self.enforcer, actual_method_name)  
  
            # Convert arguments based on method signature  
            converted_args = self._convert_arguments(method, self.args)  
  
            # Execute method  
            result = method(*converted_args)  
  
            # Build response with standardized format  
            response = ResponseBody()  
  
            # Process result based on return type 
            if isinstance(result, bool):  
                response.allow = result  
                response.explain = None
            elif isinstance(result, tuple) and len(result) == 2:  
            # Handle enforce_ex return format: (boolean, list)  
                response.allow = result[0]  
                response.explain = result[1]  
            elif isinstance(result, list):  
                response.allow = None  
                response.explain = result  
            elif hasattr(result, 'allow') and hasattr(result, 'explain'):  
                # Handle EnforceResult type  
                response.allow = result.allow  
                response.explain = result.explain  
            else:  
                response.allow = None  
                response.explain = result  


            
  
            # Save policy for modification operations  
            modification_operations = [  
                'addPolicy', 'removePolicy', 'updatePolicy',  
                'addGroupingPolicy', 'removeGroupingPolicy', 'updateGroupingPolicy',  
                'addNamedPolicy', 'removeNamedPolicy', 'addNamedPolicies', 'removeNamedPolicies',  
                'addNamedGroupingPolicy', 'removeNamedGroupingPolicy', 'addNamedGroupingPolicies',  
                'removeNamedGroupingPolicies', 'removeFilteredPolicy', 'removeFilteredNamedPolicy',  
                'removeFilteredGroupingPolicy', 'removeFilteredNamedGroupingPolicy',  
                'updateNamedGroupingPolicy', 'addRoleForUser', 'deleteRoleForUser', 'deleteRolesForUser',  
                'deleteUser', 'deleteRole', 'deletePermission', 'addPermissionForUser',  
                'deletePermissionForUser', 'deletePermissionsForUser'  
            ]  
              
            if self.command_name in modification_operations:  
                self.enforcer.save_policy()  
  
            # Return JSON response with consistent formatting  
            return json.dumps(response.to_dict(), separators=(',', ':'), ensure_ascii=False)  
  
        except Exception as e:      
            import sys  
            if hasattr(sys, '_called_from_test') or 'pytest' in sys.modules:  
                raise Exception(f"Error executing command '{self.command_name}': {str(e)}")  
            else:  
                raise Exception(f"Error executing command '{self.command_name}': {str(e)}")  
  
    def _convert_arguments(self, method, args: List[str]) -> List[Any]:  
        """Convert string arguments to appropriate types based on method signature"""  
        if not args:  
            return []

      
  
        converted = []  
          
        # Handle special cases for specific method signatures 
        if self.command_name == 'batchEnforce':
            #print(f"DEBUG: Input args: {args}")  
            #print(f"DEBUG: Args length: {len(args)}")     
            batch_requests = []  
            for arg in args:
                #print(f"DEBUG: Processing arg {i}: '{arg}'")
                split_result = arg.split(',')  
                #print(f"DEBUG: Split result: {split_result}")   
                batch_requests.append(arg.split(','))
            #print(f"DEBUG: Final batch_requests: {batch_requests}")  
            return batch_requests 
        '''
        if self.command_name == 'batchEnforce':  
            # Convert comma-separated strings to lists for batch operations
            print(f"DEBUG: Original args: {self.args}")   
            batch_requests = []  
            for arg in args:  
                if ',' in arg:  
                    batch_requests.append(arg.split(','))
                print(f"DEBUG: Converted requests: {batch_requests}") 

                try: 
                    result = self.enforcer.batch_enforce(batch_requests)  
                    print(f"DEBUG: Batch enforce result: {result}")  
                    return batch_requests   
                except Exception as e:  
                    print(f"DEBUG: Error in batch_enforce: {e}")  
                    raise 
                #else:  
                #    batch_requests.append([arg])  
            #return batch_requests 
        '''
        # Handle methods with matcher parameter  
        if self.command_name in ['enforceWithMatcher', 'enforceExWithMatcher']:  
            # First argument is matcher string, rest are regular parameters  
            converted.append(args[0])  # matcher  
            converted.extend(args[1:])  # other parameters  
            return converted  
  
        # Handle JSON object parameters  
        for i, arg in enumerate(args):  
            if arg and arg.strip().startswith('{'):  
                try:  
                    converted.append(json.loads(arg))  
                except json.JSONDecodeError:  
                    converted.append(arg)  
            elif arg and ',' in arg and self._should_split_as_list(self.command_name, i):  
                # Split comma-separated values for list parameters  
                converted.append(arg.split(','))  
            else:  
                # Handle type conversion for specific parameter types  
                converted_arg = self._convert_single_argument(arg)  
                converted.append(converted_arg)  
  
        return converted  
  
    def _should_split_as_list(self, method_name: str, arg_index: int) -> bool:  
        """Determine if an argument should be split into a list based on method and position"""  
        # Define methods that expect list parameters at specific positions  
        list_methods = {  
            'addPolicies': [0],  
            'removePolicies': [0],  
            'addNamedPolicies': [1],  
            'removeNamedPolicies': [1],  
            'addGroupingPolicies': [0],  
            'removeGroupingPolicies': [0],  
            'addNamedGroupingPolicies': [1],  
            'removeNamedGroupingPolicies': [1]  
        }  
          
        return method_name in list_methods and arg_index in list_methods[method_name]  
  
    def _convert_single_argument(self, arg: str) -> Any:  
        """Convert a single string argument to appropriate type"""  
        if arg is None:  
            return None  
              
        # Try to convert to integer  
        try:  
            return int(arg)  
        except ValueError:  
            pass  
              
        # Try to convert to boolean  
        if arg.lower() in ['true', 'false']:  
            return arg.lower() == 'true'  
              
        # Return as string  
        return arg