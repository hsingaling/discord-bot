import datetime
import os
import asyncio
from zoneinfo import ZoneInfo
import discord
from pymongo import MongoClient
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID_886_GENERAL = int(os.environ.get("CHANNEL_ID_886_GENERAL", 0))
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")

REMINDER_MESSAGE = """@everyone Please add your weekly update to the latest meeting agenda or status update doc [here](https://drive.google.com/drive/u/1/folders/1-w39d5_TnBgPrg7W0MVgJVj8bKEyByhM)"""

PST_TZ = ZoneInfo("America/Los_Angeles")

if MONGO_URI:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["discord_bot"]
    reminder_state = db["reminder_state"]
else:
    mongo_client = None
    db = None
    reminder_state = None


def load_last_sent_date():
  """Read the last reminder date from MongoDB, if configured."""
  if reminder_state is None:
    return None

  record = reminder_state.find_one({"name": "last_sent_date"})
  if record:
    return record.get("value")
  return None


def save_last_sent_date(date_string):
  """Persist the last reminder date to MongoDB."""
  if reminder_state is None:
    return

  reminder_state.update_one(
      {"name": "last_sent_date"},
      {"$set": {"value": date_string}},
      upsert=True,
  )


def clear_last_sent_date():
  """Clear the stored reminder date so a new reminder can fire later."""
  if reminder_state is None:
    return

  reminder_state.delete_one({"name": "last_sent_date"})


LAST_SENT_DATE = load_last_sent_date()

@tasks.loop(minutes=1)
async def send_weekly_reminder():
  """Send the weekly reminder once per eligible day at 5:00 PM Pacific time."""
  global LAST_SENT_DATE

  now = datetime.datetime.now(PST_TZ)
  today_key = now.date().isoformat()

  if LAST_SENT_DATE and LAST_SENT_DATE < today_key:
    clear_last_sent_date()
    LAST_SENT_DATE = None

  if now.weekday() not in (0, 1):
    if LAST_SENT_DATE is not None:
      clear_last_sent_date()
      LAST_SENT_DATE = None
    return

  if now.hour != 17 or now.minute != 30:
    return

  if LAST_SENT_DATE == today_key:
    return

  channel = bot.get_channel(CHANNEL_ID_886_GENERAL)
  if channel:
    await channel.send(REMINDER_MESSAGE)

  LAST_SENT_DATE = today_key
  save_last_sent_date(today_key)


@send_weekly_reminder.before_loop
async def before_reminder():
  """Wait until the bot is fully connected before starting the reminder loop."""
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
    target_dt = datetime.datetime.strptime(f"{target_date} {target_time}", "%Y-%m-%d %H:%M").replace(tzinfo=PST_TZ)
    now = datetime.datetime.now(PST_TZ)

    delay = (target_dt - now).total_seconds()

    if delay <= 0:
      await ctx.send("The specified time is in the past. Please choose a future date and hour.")
      return

    # Use the provided custom message if available, otherwise fall back to the default agenda message
    message_to_send = custom_message if custom_message else REMINDER_MESSAGE

    confirmation = (
        f"Reminder scheduled for {target_dt.strftime('%Y-%m-%d %H:%M')} PST. "
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