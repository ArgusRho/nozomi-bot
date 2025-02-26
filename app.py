import gradio as gr
import discord
import asyncio
import threading
import os

TOKEN = os.getenv("DISCORD_TOKEN")  # Make sure your token is in HF secrets

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Needed to read messages

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

import commands
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.lower().strip() == "hello":
        await message.channel.send("Hello! I'm hosted on Hugging Face Spaces.")
    else:
        await commands.handle_message(message)  # Forward all other messages to `commands.py`

# Function to start the bot
import sys
def run_bot():
    sys.stdin = open(os.devnull)  # Redirect stdin to prevent input errors
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(TOKEN))

# Run bot in a separate thread to prevent blocking Gradio
threading.Thread(target=run_bot, daemon=True).start()

# Simple Gradio UI to keep Spaces active
def status():
    return "Bot is running!"

iface = gr.Interface(fn=status, inputs=[], outputs="text", title="Discord Bot Status")
iface.launch(server_name="0.0.0.0", server_port=7860)

