import casbin  
import os  
import tempfile  
  
class EnforcerFactory:  
    @staticmethod  
    def create_enforcer(model_input, policy_input):  
        """Casbin Enforcer"""  
        model_path = EnforcerFactory._process_input(model_input, is_model=True)  
        policy_path = EnforcerFactory._process_input(policy_input, is_model=False)  
          
        return casbin.Enforcer(model_path, policy_path)  
      
    @staticmethod  
    def _process_input(input_str, is_model=True):  
        """Processing input can be file paths or inline content"""  
        if input_str is None:  
            raise ValueError("Input cannot be null")  
        

            # Empty string policy content is allowed, but None is not  
        if input_str.strip() == "" and not is_model:  
            # For empty policy content, create a temporary file containing empty content  
            return EnforcerFactory._write_to_temp_file("")
          
        elif input_str.strip() == "" and is_model:  
            raise ValueError("Model content cannot be empty") 
          
        # Check if it is an existing file  
        if os.path.exists(input_str) and os.path.isfile(input_str):  
            return input_str  
          
        # Verification content format  
        if is_model:  
            if not EnforcerFactory._is_valid_model_content(input_str):  
                raise ValueError("Invalid model format")  
        else:  
            if input_str.strip() and not EnforcerFactory._is_valid_policy_content(input_str):  
                raise ValueError("Invalid policy format")  
          
        # Write to a temporary file  
        return EnforcerFactory._write_to_temp_file(input_str)  
      
    @staticmethod  
    def _is_valid_model_content(content):  
        """Verify the model content format"""  
        required_sections = ['[request_definition]', '[policy_definition]',   
                           '[policy_effect]', '[matchers]']  
        return all(section in content for section in required_sections)  
      
    @staticmethod  
    def _is_valid_policy_content(content):  
        """Verify the format of the strategy content""" 
        if not content.strip():
            return True 
        lines = content.strip().split('\n')  
        return all(line.strip().startswith(('p,', 'g,')) or not line.strip()   
                  for line in lines)  
      
    @staticmethod  
    def _write_to_temp_file(content):  
        """Write the content to a temporary file"""  
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.conf') as f:  
            # Handle the delimiter  
            processed_content = content.replace('|', '\n')  
            f.write(processed_content)
            f.flush()  
            return f.name