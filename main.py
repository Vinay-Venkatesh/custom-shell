import subprocess
import sys
import os
import shutil
import shlex


def main():
    print("****************************************************")
    print("**************** Warning!!! ************************")
    print("You are logged into custom shell")
    print("All activities here will be monitored")
    print("****************************************************")
    print("****************************************************")
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()  # forces the system to write all the buffered data to standard output device.

        # Wait for user input
        # shlex.split() -> Will return first value as command and rest of the values as list and its stored in *params
        # ex: echo "hello world"
        # command - echo
        # *params - ["hello world"]
        # ex: 'custom_exec_file' file1
        # command - custom_exec_file
        # *params - file1
        command , *params = shlex.split(input())

        # A shell builtins are called from a shell, that is executed directly in the shell itself.
        # The bash shell executes the command directly, without invoking another program
        shell_built_in = [
            'echo','exit','type', 'cd', 'alias', 'bg', 'bind','break', 'builtin', 'caller', 'case', 'command', 'compgen',
            'complete', 'compopt', 'continue', 'coproc', 'declare', 'dirs', 'disown', 'enable', 'eval', 'exec', 'export', 'false', 'fc','fg', 'for', 'function', 'getopts', 'pwd'
        ]

        #
        #  match - It is similar to a switch/case statement in other languages but much more powerful,
        #  allowing you to match complex data structures and apply patterns to them
        #
        match [command]:
            case ["exit"]:
                exit()
            case ["echo"]:
                result = subprocess.run([command] + params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                print(result.stdout.strip())
            case ["type"]:
                path_to_command = shutil.which(params[0])
                if path_to_command is not None and params[0] not in shell_built_in:
                    print(f"{params[0]} is {path_to_command}")
                elif params[0] in shell_built_in:
                    print(f"{params[0]} is a shell builtin")
                else:
                    print(f"{params[0]}: not found")
            case ["pwd"]:
                print(os.getcwd())
            case ["cd"]:
                if os.path.isdir(params[0]):
                    os.chdir(params[0])
                elif params[0] == '~':
                    home_directory = os.environ.get('HOME')
                    os.chdir(home_directory)
                else:
                    print(f"cd: {params[0]}: No such file or directory")
            case _:
                # split and pass only first element to check if the command exists in the PATH (shutil)
                # Ex: custom_exec_command Alice -> Here custom_exec_command is the command and Alice is the argument
                # Steps:
                # 1. check if custom_exec_command is in the PATH
                # 2. Run the whole command using subprocess.run(custom_exec_command Alice)
                #
                #arg = command.split(" ")[0]
                path_to_command = shutil.which(command)
                if path_to_command is not None and os.access(path_to_command, os.X_OK): # os.access(path_to_command, os.X_OK) -> function to check if the path specified by path_to_command can be executed
                    result = subprocess.run([command] + params,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    print(result.stdout.strip())
                else:
                    print(f"{command}: command not found")

if __name__ == "__main__":
    main()
