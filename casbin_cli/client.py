import argparse    
import sys    
import json    
from casbin_cli.command_executor import CommandExecutor      
from casbin_cli.enforcer_factory import EnforcerFactory      
from casbin_cli.utils import process_line_breaks   
from casbin_cli.__version__ import __version__  
    
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
            elif command_name in ['-v', '--version']:    
                print(f"casbin-python-cli {__version__}")    
                print("pycasbin 1.17.0")    
                return ""  
            elif command_name == 'completion':  
                if len(args) < 2:  
                    print("Error: completion requires shell type (bash|zsh|fish)")  
                    sys.exit(1)  
                shell_type = args[1]  
                Client._generate_completion(shell_type)  
                return ""  
                
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
            if hasattr(e, '__cause__') and e.__cause__:    
                error_msg = f"{str(e)}: {str(e.__cause__)}"    
            else:    
                error_msg = str(e) if str(e) else f"{type(e).__name__}: {repr(e)}"    
          
            if hasattr(sys, '_called_from_test') or 'pytest' in sys.modules:    
                raise type(e)(error_msg) from e    
            else:    
                print(error_msg)    
                sys.exit(1)  
        
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
      completion    Generate shell completion scripts (bash|zsh|fish)  
    
    Options:    
      -m, --model <model>          The path of the model file or model text    
      -p, --policy <policy>        The path of the policy file or policy text    
      -AF, --add-function <func>   Add custom function    
    
    args:    
      Parameters required for the method    
    
    Examples:    
      casbin enforce -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv" "alice" "data1" "read"    
      casbin addPolicy -m "examples/rbac_model.conf" -p "examples/rbac_policy.csv" "alice" "data2" "write"  
      casbin completion bash > casbin_completions.bash  
"""    
        print(help_text)  
  
    @staticmethod  
    def _generate_completion(shell_type):  
        """Generate shell completion scripts"""  
        if shell_type == 'bash':  
            Client._generate_bash_completion()  
        elif shell_type == 'zsh':  
            Client._generate_zsh_completion()  
        elif shell_type == 'fish':  
            Client._generate_fish_completion()  
        else:  
            print(f"Error: Unsupported shell type '{shell_type}'. Supported: bash, zsh, fish")  
            sys.exit(1)  
  
    @staticmethod  
    def _generate_bash_completion():  
        """Generate bash completion script"""  
        # Get all available commands  
        commands = ['enforce', 'enforceEx', 'addPolicy', 'removePolicy', 'completion', 'batchEnforce',   
                   'getAllSubjects', 'getAllObjects', 'getAllActions', 'getAllRoles']  
          
        bash_script = f'''#!/bin/bash  
_casbin_completions()  
{{  
    local cur prev opts  
    COMPREPLY=()  
    cur="${{COMP_WORDS[COMP_CWORD]}}"  
    prev="${{COMP_WORDS[COMP_CWORD-1]}}"  
      
    # Master command completion  
    if [[ ${{COMP_CWORD}} == 1 ]]; then  
        opts="{' '.join(commands)}"  
        COMPREPLY=( $(compgen -W "${{opts}}" -- ${{cur}}) )  
        return 0  
    fi  
      
    # Option completion  
    case "${{prev}}" in  
        -m|--model|-p|--policy)  
            COMPREPLY=( $(compgen -f -- ${{cur}}) )  
            return 0  
            ;;  
        completion)  
            opts="bash zsh fish"  
            COMPREPLY=( $(compgen -W "${{opts}}" -- ${{cur}}) )  
            return 0  
            ;;  
    esac  
}}  
  
complete -F _casbin_completions casbin-python-cli  
'''  
        print(bash_script)  
  
    @staticmethod  
    def _generate_zsh_completion():  
        """Generate zsh completion script"""  
        commands = ['enforce', 'enforceEx', 'addPolicy', 'removePolicy', 'completion', 'batchEnforce',  
                   'getAllSubjects', 'getAllObjects', 'getAllActions', 'getAllRoles']  
          
        zsh_script = f'''#compdef casbin-python-cli  
  
_casbin_python_cli() {{  
    local context state line  
      
    _arguments -C \\  
        '1:command:({' '.join(commands)})' \\  
        '*::arg:->args'  
      
    case $state in  
        args)  
            case $words[1] in  
                completion)  
                    _arguments '1:shell:(bash zsh fish)'  
                    ;;  
                enforce|enforceEx|addPolicy|removePolicy|batchEnforce)  
                    _arguments \\  
                        '-m[model file]:file:_files' \\  
                        '--model[model file]:file:_files' \\  
                        '-p[policy file]:file:_files' \\  
                        '--policy[policy file]:file:_files'  
                    ;;  
            esac  
            ;;  
    esac  
}}  
  
_casbin_python_cli "$@"  
'''  
        print(zsh_script)  
  
    @staticmethod  
    def _generate_fish_completion():  
        """Generate fish completion script"""  
        commands = ['enforce', 'enforceEx', 'addPolicy', 'removePolicy', 'completion', 'batchEnforce',  
                   'getAllSubjects', 'getAllObjects', 'getAllActions', 'getAllRoles']  
          
        fish_script = f'''# Fish completion for casbin-python-cli  
  
# Master command completion  
complete -c casbin-python-cli -f  
  
# Command Completion  
{chr(10).join([f"complete -c casbin-python-cli -n '__fish_use_subcommand' -a '{cmd}'" for cmd in commands])}  
  
# Option completion  
complete -c casbin-python-cli -s m -l model -d 'Model file path' -r  
complete -c casbin-python-cli -s p -l policy -d 'Policy file path' -r  
  
# shell type completion for the completion subcommand  
complete -c casbin-python-cli -n '__fish_seen_subcommand_from completion' -a 'bash zsh fish'  
'''  
        print(fish_script)  
    
def main():    
    """Command line entry point"""    
    Client.run()    
    
if __name__ == "__main__":    
    main()