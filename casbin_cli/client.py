import argparse  
import sys  
import json  
from .command_executor import CommandExecutor  
from .enforcer_factory import EnforcerFactory  
from .utils import process_line_breaks  
from .__version__ import __version__
  
class Client:  
    @staticmethod  
    def run(args=None):  
        """The main entry function processes command-line parameters and performs corresponding operations"""  
        if args is None:  
            args = sys.argv[1:]  
          
        try:  
            if not args:  
                Client._print_usage_and_exit()  
                return ""  
              
            command_name = args[0]  
              
            # Handle help and version commands  
            if command_name in ['-h', '--help']:  
                Client._print_help()  
                return ""  
            #elif command_name in ['-v', '--version']:  
            #    print(f"casbin-python-cli {__version__}")  
            #    print("pycasbin 1.17.0")  
            #    return ""
              
            # Handle line breaks
            processed_args = [args[0]]  
            for i in range(1, len(args)):  
                processed_args.append(process_line_breaks(args[i]) if args[i] else None)  
              
            # Parse command-line parameters  
            parsed_args = Client._parse_args(processed_args[1:])  
              
            # enforcer  
            enforcer = EnforcerFactory.create_enforcer(  
                parsed_args.model,   
                parsed_args.policy  
            )  
              
            # Add custom functions (if any)  
            if parsed_args.add_function:  
                # Here, the functionality of custom functions can be extended  
                pass  
              
            # executive command  
            executor = CommandExecutor(enforcer, command_name, parsed_args.args)  
            result = executor.execute()  
              
            print(result)  
            return result  
              
        except Exception as e:  
            error_msg = str(e) or str(e.__cause__) if e.__cause__ else "Unknown error"  
            print(error_msg)  
            sys.exit(1)  
          
        return ""  
      
    @staticmethod  
    def _parse_args(args):  
        """Parse command-line parameters"""  
        parser = argparse.ArgumentParser(add_help=False)  
          
        parser.add_argument('-AF', '--add-function',   
                          help='Add custom function',   
                          required=False)  
          
        parser.add_argument('-m', '--model',   
                          help='The path of the model file or model text',   
                          required=True)  
          
        parser.add_argument('-p', '--policy',   
                          help='The path of the policy file or policy text',   
                          required=True)  
          
        # Parse the known parameters and use the remaining ones as command parameters  
        known_args, remaining_args = parser.parse_known_args(args)  
        known_args.args = remaining_args  
          
        return known_args  
      
    @staticmethod  
    def _print_usage_and_exit():  
        """Print the instructions for use and exit"""  
        print("Error: Command not recognized")  
        sys.exit(1)  
      
    @staticmethod  
    def _print_help():  
        """Print help information""" 
        help_text = """  
Usage: casbin [Method] [options] [args]  
  
    Casbin is a powerful and efficient open-source access control library.  
    It provides support for enforcing authorization based on various access control models.  
  
    Method:  
      enforce       Test if a 'subject' can access an 'object' with a given 'action' based on the policy  
      enforceEx     Check permissions and get which policy it matches  
      addPolicy     Add a policy rule to the policy file  
      removePolicy  Remove a policy rule from the policy file  
  
    Options:  
      -m, --model <model>          The path of the model file or model text  
      -p, --policy <policy>        The path of the policy file or policy text  
      -AF, --add-function <func>   Add custom function  
  
    args:  
      Parameters required for the method  
  
    Examples:  
      casbin enforce -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv" "alice" "data1" "read"  
      casbin addPolicy -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv" "alice" "data2" "write"  
"""  
        print(help_text)  
  
def main():  
    """Command line entry point"""  
    Client.run()  
  
if __name__ == "__main__":  
    main()