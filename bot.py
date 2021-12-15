from urllib.request import urlopen
from os import environ
import discord
import json


TOKEN = environ["BOT_TOKEN"]
JSON = environ["JSON_LINK"]
LOGO = environ["LOGO_LINK"]


def load_json():
    global data_json
    with urlopen(JSON) as j:
        data_json = json.loads(j.read().decode())


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user.name} ({self.user.id})")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        elif message.content.lower().startswith('$pdf'):
            command = message.content.split(" ", 1)
            if len(command) > 1:
                if command[1].lower() in data_json:
                    e = discord.Embed(title=data_json[command[1].lower()]["name"],
                                      url=data_json[command[1].lower()]["link"],
                                      description=data_json[command[1].lower()]["description"])
                    e.set_thumbnail(url=LOGO)
                    await message.reply(embed=e)
                else:
                    await message.reply("PDF File Not Available\nSend $available for Available PDFs")
            else:
                await message.reply("Missing Parameter\nSend $help for Help Menu")
        
        elif message.content.lower().startswith('$available'):
            backslash = "\n"
            available_message = f"""
{f"{backslash}".join([f"{x} - {data_json[x]['name']}" for x in data_json.keys()]) if data_json.keys() else "No PDFs Available"}

{f"Example: $pdf {next(iter(data_json.keys()))}" if data_json.keys() else ""}
                                 """.strip()
            await message.reply(available_message)

        elif message.content.lower().startswith('$help'):
            help_message = f"""
$pdf <name> - PDF Files
$available - Available PDFs
$help - Help Menu
$reload - Reload JSON Data
$about - About this Bot

Available PDFs: {", ".join(data_json.keys()) if data_json.keys() else "No PDFs Available"}
{f"Example: $pdf {next(iter(data_json.keys()))}" if data_json.keys() else "Example: $about"}
                            """.strip()
            await message.reply(help_message)

        elif message.content.lower().startswith('$reload'):
            load_json()
            await message.reply("JSON File Reloaded")
        
        elif message.content.lower().startswith('$about'):
            about_message = f"""
21 Consequences Discord Bot
Created by Jameel Kaisar
Source Code: <https://github.com/JameelKaisar/21Consequences-Discord-Bot>

Send $help for Help Menu
                             """.strip()
            await message.reply(about_message)


load_json()
client = MyClient()
client.run(TOKEN)
