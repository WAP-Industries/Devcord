import discord
from discord.ext import commands
import os, io, sys

class Devcord:
    Bot = commands.Bot(command_prefix="!", self_bot=True)
    Terminals = []

    class Buttons:
        Run = "⏯️"
    
    @staticmethod
    def CodeBlock(code, lang=True):
        return f"```{'python' if lang else ''}\n{code}\n```"
    
    @staticmethod
    def GetCodeResult(code):
        try:
            indexes = (lambda x: [x[0], x[-1]])(code)
            map(lambda x: x.find("```"), indexes)
            
            try:
                output = io.StringIO()
                sys.stdout = output
                exec('\n'.join(code[1:-1]))
                sys.stdout = sys.__stdout__
                output = output.getvalue()
            except Exception as e:
                output = e 
            return output
        except:
            return "Invalid formatting in code"


@Devcord.Bot.event
async def on_ready():
    print("Devcord is running")
    
@Devcord.Bot.event
async def on_thread_create(thread):
    await thread.send(Devcord.CodeBlock("# code goes here"))

@Devcord.Bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    message = await channel.fetch_message(reaction.message.id)

    if str(reaction)==str(Devcord.Buttons.Run):
        for i in reversed(range(len(Devcord.Terminals))):
            if Devcord.Terminals[i].channel.id==channel.id:
                await Devcord.Terminals[i].delete()
                Devcord.Terminals.pop(i)

        Devcord.Terminals.append(await message.reply(
            Devcord.CodeBlock(Devcord.GetCodeResult(message.content.strip().split("\n")), False),
            mention_author=True
        ))

    if str(reaction) in [str(value) for name, value in vars(Devcord.Buttons).items() if name[0]!="_"]:
        await message.remove_reaction(reaction, Devcord.Bot.user)