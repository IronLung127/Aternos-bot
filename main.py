import os
import discord
import python_aternos as aternos
import dotenv as env
import json

env.load_dotenv()
token = os.getenv('token')


class Settings:
    def __init__(self, _prefix: str, _aternos_username: str, _aternos_password: str) -> None:
        self.prefix = _prefix
        self.aternos_username = _aternos_username
        self.aternos_password = _aternos_password

def Init():
    # Settings Init:
    if os.path.exists('config.json') != True:
        open('config.json', "w").write(
            '{\n\t"prefix": ">", \n\t"aternos-password": "ask-ur-mom",\n\t"aternos-name": "ur-moms-name"\n}'
        )
    config_raw = json.load(open('config.json', "r"))
    config = Settings(config_raw['prefix'], config_raw['aternos-name'], config_raw['aternos-password'])
    
    return config

class Client(discord.Client):
    def __init__(self, _config, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.config = _config
        

    aternos = aternos.Client
    async def on_ready(self):
        print('User: ', self.user)
        

    async def on_message(self, message):
        # Ignore if it's us:
        if message.author == self.user:
            return

        if message.content.startswith(self.config.prefix):
            # Someone invoked bot command
            command = (message.content.removeprefix('>')
                       ).lower()  # remove '>' and make everything lower-case

            if command == 'help':
                print('command is help')

            elif command == 'start':
                print('Starting Server')
            elif command == 'stop':
                print('Stopping Server')

            elif command == 'setup':
                print('Setting up details for aternos server')


def main():
    config = Init()

    bot = Client(config)
    bot.run(token)


if __name__ == '__main__':
    main()