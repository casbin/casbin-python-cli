import json  
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
            # enforcer
            if not hasattr(self.enforcer, self.command_name):  
                raise AttributeError(f"Method '{self.command_name}' not found")  
              
            method = getattr(self.enforcer, self.command_name)  
              
            # calling method  
            result = method(*self.args)  
              
            # Build response  
            response = ResponseBody()  
              
            # Set the response according to the return type  
            if isinstance(result, bool):  
                response.allow = result  
            elif isinstance(result, list):  
                response.explain = result  
            elif hasattr(result, 'allow') and hasattr(result, 'explain'):  
                # EnforceResult 
                response.allow = result.allow  
                response.explain = result.explain  
            else:  
                response.explain = result  
              
            # Save strategy (if it is a modification operation)  
            if self.command_name in ['addPolicy', 'removePolicy', 'updatePolicy',   
                                   'addGroupingPolicy', 'removeGroupingPolicy']:  
                self.enforcer.save_policy()  
              
            return json.dumps(response.to_dict(), ensure_ascii=False)  
              
        except Exception as e:  
            raise Exception(f"Error executing command '{self.command_name}': {str(e)}")