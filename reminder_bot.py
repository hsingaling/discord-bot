import datetime
import os
import asyncio
import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID_886_GENERAL = int(os.environ.get("CHANNEL_ID_886_GENERAL", 0))
BOT_TOKEN = os.environ.get("BOT_TOKEN")

REMINDER_MESSAGE = """@everyone please add your update to the upcoming meeting [agenda](https://drive.google.com/drive/u/1/folders/1-w39d5_TnBgPrg7W0MVgJVj8bKEyByhM)

Format:
1. FYI - Ready only. Includes status update or completed tasks that are easy to understand. 
2. Updates (<2min per) - Brief updates that may need quick input from the team(1 -2 questions) from the group.
3. Discussion (<10min per) - Topics that require lengthy team input should go here."""

@tasks.loop(time=datetime.time(hour=17, minute=0, tzinfo=datetime.timezone.utc))
async def send_weekly_reminder():
  """Runs at 17:00 UTC every day and sends the agenda reminder only
  on Monday and Tuesday.
  """
  today = datetime.datetime.now(datetime.timezone.utc)
  if today.weekday() in (0, 1):
    channel = bot.get_channel(CHANNEL_ID_886_GENERAL)
    if channel:
      await channel.send(REMINDER_MESSAGE)


@send_weekly_reminder.before_loop
async def before_reminder():
  """Pauses exec# Discord Weekly Reminder Bot

A lightweight Discord bot that automatically sends a weekly agenda reminder every Tuesday, with support for scheduled custom reminders. **Please note that this bot currently applies exclusively to the general channel (`CHANNEL_ID_886_GENERAL`)[cite: 1].**

---

## Features

- **Automated Weekly Reminders:** Runs a background loop to post the agenda reminder automatically every Tuesday[cite: 1].
- **Scheduled Custom Reminders:** Allows administrators to schedule a reminder for a specific date and time using a chat command[cite: 1].
- **Environment Variable Configuration:** Securely pulls the bot token and channel ID from environment variables[cite: 1].

---

## Environment Variables

To run this bot, you must configure the following environment variables (via your hosting provider like Render, or a local `.env` file)[cite: 1]:

- `BOT_TOKEN`: Your Discord bot token from the Discord Developer Portal[cite: 1].
- `CHANNEL_ID_886_GENERAL`: The numeric ID of the general Discord text channel where reminders will be sent[cite: 1].

---

## Setup & Running Locally

1. **Install Dependencies:**
   ```bash
   pip install discord.pyution until the bot is fully logged in and ready
  before starting the background loop.
  """
  await bot.wait_until_ready()


@bot.event
async def on_ready():
  """Triggered once the bot successfully connects to Discord,
  prints a login confirmation, and kicks off the background task.
  """
  print(f"Logged in as {bot.user}")
  send_weekly_reminder.start()


@bot.command(name="sendreminder")
@commands.has_permissions(administrator=True)
async def manual_reminder(ctx, target_date: str, target_time: str, *, custom_message: str = None):
  """Allows server administrators to schedule a custom reminder for a specific 
  date and hour. Usage: !sendreminder YYYY-MM-DD HH:MM [Your custom message]
  """
  try:
    target_dt = datetime.datetime.strptime(f"{target_date} {target_time}", "%Y-%m-%d %H:%M")
    now = datetime.datetime.utcnow()

    delay = (target_dt - now).total_seconds()

    if delay <= 0:
      await ctx.send("The specified time is in the past. Please choose a future date and hour.")
      return

    # Use the provided custom message if available, otherwise fall back to the default agenda message
    message_to_send = custom_message if custom_message else REMINDER_MESSAGE

    confirmation = (
        f"Reminder scheduled for {target_dt} UTC. "
        f"I’ll post it in <#{CHANNEL_ID_886_GENERAL}> when the time arrives."
    )
    await ctx.send(confirmation)

    await asyncio.sleep(delay)

    channel = bot.get_channel(CHANNEL_ID_886_GENERAL)
    if channel:
      await channel.send(message_to_send)
    else:
      await ctx.send(message_to_send)

  except ValueError:
    await ctx.send("Invalid format! Please use: `!sendreminder YYYY-MM-DD HH:MM [Message]`")


bot.run(BOT_TOKEN)