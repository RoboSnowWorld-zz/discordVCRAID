# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
import multiprocessing

import commands
import voice_raid
import discord
import os
current_path = os.path.dirname(os.path.realpath(__file__))

try:
    f = open(current_path + "/" + "workingtokens.txt")
except FileNotFoundError:
    print("[WARN] \x1b[31;1mworkingtokens.txt not found\x1b[39;49m \n")


print('Discord voice tool by RoboSnowWorld \n')

while True:
    command = input()
    try:
        commands.globals[command.split()[0]](command)
    except KeyError:
        print("\x1b[31;1mUnknown command. Type help to see commands description\x1b[39;49m")
    except IndexError:
        pass

