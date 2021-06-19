import voice_raid

globals = {
    'tokens': voice_raid.tokens,
    'music': voice_raid.music,
    'help': voice_raid.show_help,
    'exit': voice_raid.exit_raidtool,
}

tokens = {
    'join': voice_raid.join,
    'check': voice_raid.check_tokens,
    'join_queue': voice_raid.join_queue,
    'stop': voice_raid.stop,
    'invite': voice_raid.set_invite_link,
}

music = {
    'set': voice_raid.set_music,
}

description = {
    'tokens join [channel_id]': 'All tokens enter the room at the same time and play music',
    'tokens check [file]': 'Check your tokens',
    'tokens stop': 'Stop raiding',
    'tokens join_queue [delay]': 'Bots take turns entering the channel(s) at the specified interval. You need to '
                                 'specify Channel(s) ID in the channels.txt',
    'music set [file]': 'Set music to play',
    'tokens invite [link]': 'Set invite link',
    'exit': 'close raidtool',
}