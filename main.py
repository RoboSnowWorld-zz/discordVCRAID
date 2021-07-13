import commands
import os
dirname = os.path.dirname(__file__)
working_tokens_path = os.path.join(dirname, 'workingtokens.txt')

try:
    f = open(working_tokens_path)
    f.close()
except FileNotFoundError:
    print("[WARN] \x1b[31;1mworkingtokens.txt not found\x1b[39;49m \n")


print('Discord voice tool by RoboSnowWorld \n')

while True:
    command = input()
    try:
        commands.global_cmds[command.split()[0]](command)
    except KeyError:
        print("\x1b[31;1mUnknown command. Type help to see commands description\x1b[39;49m")
    except IndexError:
        pass

