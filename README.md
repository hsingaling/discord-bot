# Discord Reminder Bot

A Discord bot that posts the team agenda reminder on Monday and Tuesday at 5:00 PM UTC and also supports one-off custom reminders scheduled by administrators.

> **Single-channel only:** the bot only ever posts to one hardcoded channel (set via `CHANNEL_ID_886_GENERAL`). It cannot be configured to post to multiple channels or servers without code changes.

## How it works

- **Recurring reminder:** the bot runs daily at 17:00 UTC and posts the default agenda reminder only when the current day is Monday or Tuesday.
- **Custom scheduled reminder:** server administrators can run `!sendreminder` in any channel to schedule a one-time reminder (default or custom message) for a specific future date/time. The bot waits until that time, then posts the message to the configured channel.

### Commands

`!sendreminder YYYY-MM-DD HH:MM [custom message]`

- Requires Administrator permission.
- Date/time is interpreted as UTC.
- If `custom message` is omitted, the default agenda message is used.
- Must be a future date/time.

**Examples:**

```bash
!sendreminder 2026-09-15 09:00
```
Schedules the default agenda reminder for 2026-09-15 at 09:00 UTC.

```bash
!sendreminder 2026-09-15 09:00 Don't forget to submit your timesheets by Friday!
```
Schedules a custom message for 2026-09-15 at 09:00 UTC.

```bash
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

## Notes

- The recurring reminder is intentionally limited to Monday and Tuesday at 5:00 PM UTC.
- The bot posts in a single configured channel and does not currently support multi-channel or multi-server deployment.
