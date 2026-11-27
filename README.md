# CS-193 Final Project: D&D Campaign Manager Discord Bot

A Discord bot that helps players keep track of Dungeons & Dragons campaigns, character profiles, notes, and dice rolls all in one place.

## The Problem

As someone who plays Dungeons & Dragons, I often found myself storing character information in several different places. Notes might be in Discord messages, character details might be in a document somewhere else, and campaign information can quickly become difficult to keep organized.

The goal of this project is to make it easier to keep track of everything in one place. Instead of jumping between files and notes, users can manage campaigns and character information directly through Discord commands.

The bot also includes a dice roller so it can be used during gameplay as well.

## How It Works

The bot runs through Discord and responds to user commands.

Users can create campaigns, add characters to those campaigns, update information such as race or notes, and view character profiles through Discord embeds. Character and campaign information is stored in a JSON file so data is not lost when the bot shuts down.

When a command is used:

1. Discord sends the command to the bot.
2. The bot processes the input.
3. Character or campaign data is updated or retrieved.
4. Changes are saved to `characters.json`.
5. The bot responds with a message or a character profile embed.

### System Diagram

![System Diagram](https://raw.githubusercontent.com/abbyhughess/cs-193-final-project/43abf528cdd48da41ce2e0c7752c536e1dbe0ac6/diagram.drawio.svg)

## Tech Stack

### Language

- Python

### Libraries

- discord.py
- json
- random
- os

### External Tools

- GitHub
- Discord Developer Portal
- PyCharm

### Data Storage

- Local JSON file (`characters.json`)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/abbyhughess/cs-193-final-project.git
```

### 2. Navigate to the Project Directory

```bash
cd cs-193-final-project
```

### 3. Install Dependencies

```bash
pip install discord.py
```

### 4. Create a Discord Bot

1. Go to the Discord Developer Portal.
2. Create a new application.
3. Open the **Bot** tab.
4. Create a bot user.
5. Enable **Message Content Intent**.
6. Copy your bot token.

### 5. Add Your Token

Open `discordbot.py` and replace:

```python
TOKEN = "REPLACE_WITH_YOUR_TOKEN"
```

with your own token.

### Important

Never share your bot token publicly.

If someone else gets access to your token, they can control your bot. If a token is accidentally exposed, reset it immediately through the Discord Developer Portal.

### 6. Start the Bot

Run:

```bash
python .\final_project\src\discordbot.py
```

If everything works correctly, you should see:

```text
Logged in as BotName
```

in your terminal.

## Example Usage

### Create a Campaign

Input:

```text
!newcampaign Curse of Strahd
```

Output:

```text
Campaign 'Curse of Strahd' created.
```

### Add a Character

Input:

```text
!addcharacter "Curse of Strahd" Thorin Paladin 5
```

Output:

```text
Thorin added to Curse of Strahd.
```

### View a Character

Input:

```text
!character "Curse of Strahd" Thorin
```

Output:

A Discord embed displaying the character's:
- Name
- Class
- Level
- Race
- Notes
- Portrait image (if one is set)

### Roll Dice

Input:

```text
!roll 1 20 5
```

Output:

```text
Base Roll: 14
Modifier: 5
Final Roll: 19
```

## Roadmap

### Completed

- [x] Set up Git repository
- [x] Create Discord bot
- [x] Connect bot to Discord
- [x] Implement custom commands
- [x] Create campaigns
- [x] Delete campaigns
- [x] List campaigns
- [x] Create character profiles
- [x] Delete character profiles
- [x] Store character race information
- [x] Store character notes
- [x] Store portrait image URLs
- [x] Save data to JSON
- [x] Load data from JSON
- [x] Create custom dice roller
- [x] Display character profiles using embeds

### Future Improvements

- [ ] Direct image uploads instead of URLs
- [ ] Inventory tracking
- [ ] Hit point tracking
- [ ] Initiative rolling
- [ ] Edit character names and classes
- [ ] Support multiple Discord servers with isolated data
- [ ] Public hosting
- [ ] Slash command support

## Demo

Video Walkthrough:

![Video Walkthrough](https://youtu.be/rVwp9bc03Pg)

## Notes

Campaign names that contain spaces should be placed inside quotation marks.

Example:

```text
!campaign "Curse of Strahd"
```

```text
!character "Curse of Strahd" Thorin
```

For character portraits, image-hosting sites such as Catbox are recommended because they provide direct image URLs that Discord can display properly.
