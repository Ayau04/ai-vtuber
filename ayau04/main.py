from twitchio.ext import commands
from chat import *
import vlc
import os 
import time
import nltk
import creds

CONVERSATION_LIMIT = 20

class Bot(commands.Bot):

    conversation = list()

    def __init__(self):
        Bot.conversation.append({'role': 'system', 'content': open_file('prompt_chat.txt')})
        super().__init__(token=creds.TWITCH_TOKEN, prefix='!', initial_channels=[creds.TWITCH_CHANNEL])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        nltk.download('words')
        if not any(word in message.content for word in nltk.corpus.words.words()):
            return
        if len(message.content) > 70 or len(message.content) < 3:
            return

        print('------------------------------------------------------')
        print(message.content)
        print(message.author.name)
        print(Bot.conversation)

        content = message.content.encode(encoding='ASCII', errors='ignore').decode()
        Bot.conversation.append({'role': 'user', 'content': content})
        print(content)

        response = groq_completion(Bot.conversation)
        print('DOGGIEBRO:', response)

        if Bot.conversation.count({'role': 'assistant', 'content': response}) == 0:
            Bot.conversation.append({'role': 'assistant', 'content': response})

        if len(Bot.conversation) > CONVERSATION_LIMIT:
            Bot.conversation = Bot.conversation[1:]

        speak_text(response)
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')

bot = Bot()
bot.run()
