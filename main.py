import discord as chat
import os
import python_aternos as aternos
import dotenv as env
import json
from time import sleep

env.load_dotenv()
token = os.getenv('token')


class Settings:

	def __init__(self, _prefix: str, _aternos_username: str,
				 _aternos_password: str) -> None:
		self.prefix = _prefix
		self.aternos_username = _aternos_username
		self.aternos_password = _aternos_password
	
def Init():
	# Settings Init:
	if os.path.exists('config.json') != True:
		open('config.json', "w").write(
			'{\n\t"prefix": ">", \n\t"aternos-password": "placeHolderPassword",\n\t"aternos-name": "placeHoldeUsername"\n}'
		)
	config_raw = json.load(open('config.json', "r"))
	config = Settings(config_raw['prefix'], config_raw['aternos-name'],
					  config_raw['aternos-password'])

	return config


class Client(chat.Client):

	def UpdateSettings(self, _prefix, _aternos_username, _aternos_password):
			self.config.prefix = _prefix         
			self.config.aternos_username = _aternos_username
			self.config.aternos_password = _aternos_password

			config_raw = {
				"prefix": self.config.prefix,
				"aternos-password": self.config.aternos_password,
				"aternos-name": self.config.aternos_username
			}

			open('config.json', 'w').write(json.dumps(config_raw, indent=4, sort_keys=True))
			

	def __init__(self, _config, *, loop=None, **options):
		super().__init__(loop=loop, **options)
		self.config: Settings = _config
		self.aternosAPI = aternos.Client


	async def on_ready(self):
		print('User: ', self.user)

	async def on_message(self, message):
		# Ignore if it's us:

		if message.author == self.user:
			return

		if message.content.startswith(self.config.prefix):
			# Someone invoked bot command
			command = (message.content.removeprefix(self.config.prefix)
					   ).lower()  # remove '>' and make everything lower-case

			if command.startswith('help'):
				print('command is help')

			elif command.startswith('start'):
				print('Starting Server')
			elif command == 'stop':
				print('Stopping Server')

			elif command == 'setup help':
				await message.channel.send(
					'Type `' + self.config.prefix +
					'setup *your_aternos_username* *your_aternos_password*`')

			elif command.startswith('setup'):
				message_array = message.content.split()
				self.UpdateSettings(self.config.prefix, message_array[1], message_array[2])
				

				await message.delete()

def main():
	config = Init()

	bot = Client(config)
	bot.run(token)


if __name__ == '__main__':
	main()