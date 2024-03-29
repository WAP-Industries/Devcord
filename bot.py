import discord
from discord.ext import commands
import os, shutil, subprocess

class Devcord:
    Bot = commands.Bot(command_prefix="!", self_bot=True)
    CodeBlocks = []
    Terminals = []

    class Settings:
        RunButton = "⏯️"
        StartCode = "# code goes here"
    
    @staticmethod
    def CodeBlock(code, lang=True):
        return f"```{['', 'python'][lang]}\n{code or ' '}\n```"
    
    @staticmethod
    def ParseCode(code):
        code = code.strip().split("\n")
        try:
            [i.index("```") for i in [code[0], code[-1]]]
            start, end = 1, -1
        except:
            start, end = 0, len(code)
        return '\n'.join(code[start:end]), start

    @staticmethod
    def GetCodeResult(raw, file):
        if not Devcord.ParseCode(raw)[1]:
            return "Invalid formatting in code block"
        try:
            result = subprocess.run(["python", file], capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            result = e
        return f"{result.stdout}{result.stderr}"
        

@Devcord.Bot.event
async def on_ready():
    print("Devcord is running")


@Devcord.Bot.event
async def on_guild_channel_create(channel):
    if not os.path.exists(channel.name):
        os.mkdir(channel.name)

@Devcord.Bot.event
async def on_guild_channel_delete(channel):
    Devcord.CodeBlocks = [i for i in Devcord.CodeBlocks if i.channel.channel]
    try:
        shutil.rmtree(channel.name)
    except:
        pass

@Devcord.Bot.event
async def on_guild_channel_update(before, after):
    if before.name!=after.name:
        os.rename(f"{before.name}\\", f"{after.name}\\")

    
@Devcord.Bot.event
async def on_thread_create(thread):
    if not os.path.exists(thread.channel.name):
        os.mkdir(thread.channel.name)
    message = await thread.send(Devcord.CodeBlock(Devcord.Settings.StartCode))
    Devcord.CodeBlocks.append(message)
    with open(f"{thread.channel.name}\\{thread.name}", "w") as f:
        f.write(Devcord.Settings.StartCode)

@Devcord.Bot.event
async def on_thread_delete(thread):
    Devcord.CodeBlocks = [i for i in Devcord.CodeBlocks if i.channel.id!=thread.id]
    try:
        os.remove(f"{thread.channel.name}\\{thread.name}")
    except:
        pass

@Devcord.Bot.event
async def on_thread_update(before, after):
    if before.name!=after.name:
        os.rename(f"{before.channel.name}\\{before.name}", f"{after.channel.name}\\{after.name}")


@Devcord.Bot.event
async def on_message_edit(_, after):
    if not after in Devcord.CodeBlocks:
        return
    with open(f"{after.channel.channel.name}\\{after.channel.name}", "w") as f:
        f.write(Devcord.ParseCode(after.content)[0])


@Devcord.Bot.event
async def on_reaction_add(reaction, _):
    if not reaction.message in Devcord.CodeBlocks:
        return

    channel = reaction.message.channel
    message = await channel.fetch_message(reaction.message.id)

    if str(reaction)==str(Devcord.Settings.RunButton):
        for i in reversed(range(len(Devcord.Terminals))):
            if Devcord.Terminals[i].channel.id==channel.id:
                await Devcord.Terminals[i].delete()
                Devcord.Terminals.pop(i)

        Devcord.Terminals.append(await message.reply(
            Devcord.CodeBlock(
                Devcord.GetCodeResult(message.content, f"{message.channel.channel.name}\\{message.channel.name}"), 
                False
            ),
            mention_author=True
        ))

        await message.remove_reaction(reaction, Devcord.Bot.user)