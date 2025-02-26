import discord
import chatbot
import asyncio
from datetime import datetime, timedelta

prefix = "!"
alarms = {}  # Stores alarms as {user_id: (alarm_time, message)}

async def handle_message(message):
    """Handles all commands except 'hello'."""
    
    content = message.content.lower().strip()

    if content.startswith(f"{prefix}echo"):
        await echo(message)
    elif content.startswith(f"{prefix}avatar"):
        await avatar(message)
    elif content.startswith(f"{prefix}alarm"):
        await set_alarm(message)
    elif content.startswith(f"{prefix}i"):
        print("［System］ignored a message")
    else:
        await chatbot.respond_to_message(message)  # Forward normal messages to AI bot

async def echo(message):
    """Repeats the user message."""
    args = message.content.split(" ", 1)
    if len(args) == 1:
        await message.channel.send("You need to provide a message to echo!😐")
    else:
        await message.channel.send(args[1])

async def avatar(message):
    """Sends the user's avatar URL."""
    user = message.mentions[0] if message.mentions else message.author
    await message.channel.send(f"{user.display_name}'s avatar: {user.display_avatar.url}")

async def set_alarm(message):
    """Set an alarm with a custom message for the user."""
    args = message.content.split(" ", 2)

    if len(args) < 2:
        await message.channel.send("Usage: `!alarm <minutes> [optional message]`\nExample: `!alarm 5 Take a break!`")
        return

    if not args[1].isdigit():
        await message.channel.send("Please enter a valid number of minutes.")
        return

    minutes = int(args[1])
    
    if len(args) > 2:
        user_message = args[2]
    else:
        user_message = "✌️"

    alarm_time = datetime.utcnow() + timedelta(minutes=minutes)
    user_id = message.author.id
    alarms[user_id] = (alarm_time, user_message)

    await message.channel.send(f"⏰ Alarm set for <@{user_id}> in {minutes} minutes.\n{user_message}")

    # Wait until alarm time and ping the user
    await asyncio.sleep(minutes * 60)
    if user_id in alarms and alarms[user_id][0] == alarm_time:
        await message.channel.send(f"⏰ Hey <@{user_id}>, your alarm is ringing!💢\n{user_message}")
        del alarms[user_id]