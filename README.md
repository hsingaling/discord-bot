# Discord Reminder Bot

A Discord bot that posts the team agenda reminder on Monday and Tuesday at 5:30 PM Pacific Time (PST), and also supports one-off custom reminders scheduled by administrators.

> **Single-channel only:** the bot always posts to one hardcoded channel defined by `CHANNEL_ID_886_GENERAL`. It does not currently support multi-channel or multi-server output without code changes.

## How it works

- **Recurring reminder:** the bot checks once per minute and sends the default agenda reminder only when it is Monday or Tuesday at 5:30 PM PST.
- **Duplicate prevention:** the bot stores the last reminder date in MongoDB so it does not send the same reminder more than once per day.
- **Custom scheduled reminder:** server administrators can run `!sendreminder` in any channel to schedule a one-time reminder for a specific future date/time. The bot waits until that time and then posts the message to the configured channel.

### Commands

`!sendreminder YYYY-MM-DD HH:MM [custom message]`

- Requires Administrator permission.
- Date/time is interpreted in PST.
- If `custom message` is omitted, the default agenda message is used.
- Must be a future date/time.

**Examples:**

```bash
!sendreminder 2026-09-15 09:00
```
Schedules the default agenda reminder for 2026-09-15 at 09:00 PST.

```bash
!sendreminder 2026-09-15 09:00 Don't forget to submit your timesheets by Friday!
```
Schedules a custom message for 2026-09-15 at 09:00 PST.

```bash
!sendreminder 2026-12-24 17:30 Reminder: office closes early today at 5:30pm PST.
```
Schedules a one-off holiday reminder.

## Requirements

- Python 3.14+
- [`discord.py`](https://pypi.org/project/discord.py/) >= 2.7.1
- [`pymongo`](https://pymongo.readthedocs.io/en/stable/) >= 4.9.0
- A Discord bot application/token with the **Message Content** intent enabled in the Discord Developer Portal
- A MongoDB connection string for reminder persistence

Dependencies are managed with [uv](https://docs.astral.sh/uv/) (see `pyproject.toml`).

## Environment variables

| Variable | Description |
|---|---|
| `BOT_TOKEN` | Your Discord bot token from the Discord Developer Portal |
| `CHANNEL_ID_886_GENERAL` | The numeric ID of the single channel the bot posts reminders to |
| `MONGO_URI` | MongoDB connection string used to persist the last reminder date |

## Setup & running locally

1. Install dependencies:
   ```bash
   uv sync
   ```
2. Set the required environment variables:
   ```bash
   export BOT_TOKEN=your_bot_token
   export CHANNEL_ID_886_GENERAL=your_channel_id
   export MONGO_URI="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
   ```
3. Run the bot:
   ```bash
   uv run reminder_bot.py
   ```

## Notes

- The recurring reminder is intentionally limited to Monday and Tuesday at 5:30 PM PST.
- The bot posts in a single configured channel and does not currently support multi-channel or multi-server deployment.
- If `MONGO_URI` is not set, the bot falls back to in-memory tracking only, which is not persistent across restarts.
