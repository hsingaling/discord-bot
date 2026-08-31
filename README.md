# Discord Reminder Bot

A Discord bot that posts a recurring weekly agenda reminder and lets admins schedule one-off custom reminders.

> **Single-channel only:** the bot only ever posts to one hardcoded channel (set via `CHANNEL_ID_886_GENERAL`). It cannot be configured to post to multiple channels or servers without code changes.

## How it works

- **Weekly reminder:** a background loop checks once every 24 hours whether the current UTC day is Tuesday, and if so posts the default agenda reminder message to the configured channel.
- **Custom scheduled reminder:** server administrators can run `!sendreminder` in any channel to schedule a one-time reminder (default or custom message) for a specific future date/time. The bot sleeps until that time, then posts the message to the configured channel.

### Commands

`!sendreminder YYYY-MM-DD HH:MM [custom message]`

- Requires Administrator permission.
- Date/time is interpreted as UTC.
- If `custom message` is omitted, the default weekly agenda message is used.
- Must be a future date/time.

**Examples:**

```
!sendreminder 2026-09-15 09:00
```
Schedules the default weekly agenda message for 2026-09-15 at 09:00 UTC.

```
!sendreminder 2026-09-15 09:00 Don't forget to submit your timesheets by Friday!
```
Schedules a custom message for 2026-09-15 at 09:00 UTC.

```
!sendreminder 2026-12-24 17:30 Reminder: office closes early today at 5:30pm UTC.
```
Schedules a one-off holiday reminder.

## Requirements

- Python 3.14+
- [`discord.py`](https://pypi.org/project/discord.py/) >= 2.7.1
- A Discord bot application/token with the **Message Content** intent enabled in the Discord Developer Portal

Dependencies are managed with [uv](https://docs.astral.sh/uv/) (see `pyproject.toml` / `uv.lock`).

## Environment variables

| Variable | Description |
|---|---|
| `BOT_TOKEN` | Your Discord bot token from the Discord Developer Portal |
| `CHANNEL_ID_886_GENERAL` | The numeric ID of the single channel the bot posts reminders to |

## Setup & running locally

1. Install dependencies:
   ```bash
   uv sync
   ```
2. Set the required environment variables:
   ```bash
   export BOT_TOKEN=your_bot_token
   export CHANNEL_ID_886_GENERAL=your_channel_id
   ```
3. Run the bot:
   ```bash
   uv run reminder_bot.py
   ```
