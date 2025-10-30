# 67-Negator <img src="https://img.shields.io/github/followers/MicahXX?style=for-the-badge" alt="Followers Badge"/> <img src="https://img.shields.io/github/stars/MicahXX/67-Negator?style=for-the-badge" alt="Stars Badge"/>

A small Discord moderation bot that purposefully deletes any message containing the string "67".

## Table of contents
- Features
- Requirements
- Installation
- Quick start
- Behavior
- Configuration
- Troubleshooting
- Links
- Author

## Features
- Automatically deletes any message containing "67" (intentional behavior).
- Lightweight, pure-Python bot.
- Easy configuration via environment variable.

## Requirements
- Python 3.8+
- A Discord bot token and a server where you have permission to add bots.

## Installation
```bash
git clone https://github.com/MicahXX/67-Negator.git
cd 67-Negator
```

## Quick start
1. Go to a website like Railway make an Account and set a Variable with the name Token,
with the value of the Token, with your cloned repo. OR
2.
```bash
from dotenv import load_dotenv  # new import

load_dotenv()  # loads variables from .env

TOKEN = os.getenv("TOKEN")  # reads the token

bot.run(TOKEN) # update last line
```
And run the bot localy.

## Behavior
- The bot listens to messages and deletes any message that contains the substring "67". This is the primary, intentional behavior of the project.
- Use in servers where this moderation rule is desired.

## Configuration
- TOKEN — Discord bot token (required).

## Troubleshooting
- Bot won't start / token errors: ensure TOKEN is set and the token is valid.

## Links
- Repository: https://github.com/MicahXX/67-Negator
- Author: https://github.com/MicahXX

## Author
Made by MicahCode (MicahXX)
