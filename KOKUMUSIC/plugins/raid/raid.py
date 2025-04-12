import asyncio
from random import choice
from pyrogram import Client, filters
from pyrogram.types import Message

from KOKUMUSIC.misc import SUDOERS as SUDO_USER
from KOKUMUSIC.cplugin.utils.data import RAID, PBIRAID, OneWord, HIRAID, GROUP, VERIFIED_USERS

async def get_target_user(client, message, args):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    elif len(args) >= 3:
        try:
            return await client.get_users(args[2])
        except:
            return None
    return None

async def handle_spam_command(client, message, wordlist, cmd_name):
    args = message.text.split()

    if len(args) < 2 and not message.reply_to_message:
        return await message.reply_text(f"Usage: .{cmd_name} count @username or reply")

    try:
        count = int(args[1])
    except:
        return await message.reply_text("Please provide a valid count number.")

    user = await get_target_user(client, message, args)
    if not user:
        return await message.reply_text("User not found or reply missing.")

    if message.chat.id in GROUP:
        return await message.reply_text("**Sorry! I can't spam in this group.**")
    if user.id in VERIFIED_USERS:
        return await message.reply_text("This user is my developer.")
    if user.id in SUDO_USER:
        return await message.reply_text("Sorry, I can't raid this user because they are a sudo user.")

    mention = user.mention
    for _ in range(count):
        msg = f"{mention} {choice(wordlist)}"
        await client.send_message(message.chat.id, msg)
        await asyncio.sleep(0.3)

# RAID
@Client.on_message(filters.command("raid", prefixes=".") & SUDO_USER)
async def raid_command(client: Client, message: Message):
    await handle_spam_command(client, message, RAID, "raid")

# PBIRAID
@Client.on_message(filters.command("pbiraid", prefixes=".") & SUDO_USER)
async def pbiraid_command(client: Client, message: Message):
    await handle_spam_command(client, message, PBIRAID, "pbiraid")

# ONEWORD
@Client.on_message(filters.command("oneword", prefixes=".") & SUDO_USER)
async def oneword_command(client: Client, message: Message):
    await handle_spam_command(client, message, OneWord, "oneword")

# HIRAID
@Client.on_message(filters.command("hiraid", prefixes=".") & SUDO_USER)
async def hiraid_command(client: Client, message: Message):
    await handle_spam_command(client, message, HIRAID, "hiraid")
