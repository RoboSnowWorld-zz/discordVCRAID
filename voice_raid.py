import tracemalloc
import os.path
import discord
import time
import requests
import multiprocessing
import logging
import proxygen
from itertools import cycle

import checker
import commands

tracemalloc.start()
proxies = proxygen.get_proxies()
proxy_pool = cycle(proxies)
music_file = ''
channels = []
token_list = []
bots = []
invite_link = ''
channel_id = 0
delay = 8
connection_process = ''
current_path = os.path.dirname(os.path.realpath(__file__))
token_dict = {}

logging.basicConfig(filename="errors.log", level=logging.ERROR, filemode='w')

apilink = "https://discordapp.com/api/v6/invite"


def tokens(command):
    global token_list
    global channels
    token_list = []
    channels = []
    try:
        f = open(current_path + "/" + "workingtokens.txt")
        for line in f.read().splitlines():  # read rest of lines
            token_list.append(line)
        f.close()
    except FileNotFoundError:
        print("Pls, check your tokens (tokens check [file])")
    commands.tokens[command.split()[1]](command)


def music(command):
    commands.music[command.split()[1]](command)


def join(command):
    global channels
    global invite_link
    try:
        channels.append(command.split()[2])
    except IndexError:
        print('tokens join [channel_id]')
        return
    args = 'join'
    try:
        add_arg = command.split()[3]
        args += add_arg
        invite_link = command.split()[4]
    except IndexError:
        pass

    global connection_process
    connection_process = multiprocessing.Process(target=connect, args=(args,))
    connection_process.start()


def show_help(message):
    for command in commands.description:
        print(command, ' - ', commands.description[command])


def stop(command):
    for bot in bots:
        bot.kill()
    connection_process.kill()
    print('\x1b[32;1mSuccessfully\x1b[39;49m')


def check_tokens(command):
    try:
        file = command.split()[2]
        checker.check(file)
    except IndexError:
        print('tokens check [file]')
        return
    except FileNotFoundError:
        print('File must be in discordVCRAID folder \n')
        print('Filename must be with file extension. Example: tokens check tokens.txt \n')
        print('tokens check [file]')


def set_invite_link(command):
    global invite_link
    try:
        invite = command.split()[2]
    except IndexError:
        print("tokens join [invite_link]")
        return
    apiinvite = 'https://discordapp.com/api/v6/invite/'
    inv_code = invite.split('/')
    apiinvite += inv_code[len(inv_code) - 1]
    invite_link = apiinvite
    print(invite_link)
    print("\x1b[32;1mSuccessfully\x1b[39;49m")


def join_queue(command):
    try:
        global delay
        delay = int(command.split()[2])
        f = open(current_path + '/' + 'channels.txt')
        for channel in f.read().splitlines():
            channels.append(channel)
        f.close()
    except FileNotFoundError:
        print("File channels.txt not found\n")
        print("File must be in discordVCRAID folder\n")
        print("In this file you put channel(s) ID for raid\n")
        return
    except ValueError or IndexError:
        pass

    args = 'join_queue'
    global connection_process
    connection_process = multiprocessing.Process(target=connect, args=(args,))
    connection_process.start()


def connect(run_args):
    if music_file:
        for token in token_list:
            client = Bot()
            token_dict[client] = token
            bot = multiprocessing.Process(target=client.run, args=(token,), kwargs={'bot': False})
            bot.start()
            bots.append(bot)
            global delay
            if 'join_queue' in run_args: time.sleep(delay + 1)
    else:
        print("\x1b[31;1mSet music file - music set [file]\x1b[39;49m")


def set_music(command):
    global music_file
    try:
        music_file = command.split()[2]
        f = open(current_path + "/" + music_file, 'rb')
        f.close()
        print(f'\x1b[32;1mSuccessfully\x1b[39;49m')
    except IndexError:
        print('music set [file]')
    except FileNotFoundError:
        print('File must be in discordVCRAID folder \n')
        print('Filename must be with file extension. Example: tokens check tokens.txt \n')
        print('music set [file]')


class Bot(discord.Client):
    async def on_ready(self):
        print("[LOG] Client is ready")
        global channels
        global delay
        for ch_id in channels:
            ch_id = int(ch_id)
            if invite_link:
                proxy = 'http://' + next(proxy_pool)
                token = token_dict[self]
                headers = {
                    "authorization": token,
                }
                r = requests.post(invite_link, headers=headers, proxies={'http': proxy})
                print('[LOG]', r)
                if r.status_code == 200:
                    print("[LOG] Bot joined server")
                else: print("[WARN]\x1b[31;1m Cannot join the server. Try to change IP or use another tokens\x1b[39;49m")
            try:
                channel = await self.fetch_channel(ch_id)
                vc = await channel.connect()
                vc.play(discord.FFmpegPCMAudio(
                    source=current_path + '/' + music_file))
                print("[LOG] Bot entered the room")
                time.sleep(delay)
                await vc.disconnect()
            except discord.errors.Forbidden:
                print('[WARN]\x1b[31;1m Cannot join the room\x1b[39;49m')
            await self.close()
