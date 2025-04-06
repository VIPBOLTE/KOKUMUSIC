import random
import asyncio
from random import choice
from pyrogram import Client, filters
from pyrogram.types import Message
from KOKUMUSIC.misc import SUDOERS as SUDO_USER
from KOKUMUSIC.cplugin.utils.data import HIRAID, GROUP, VERIFIED_USERS

@Client.on_message(filters.command("hiraid", prefixes=".") & SUDO_USER)
async def hiraid(client: Client, m: Message):  
    # Check if enough arguments are provided or if it's a reply
    if len(m.command) < 2 and not m.reply_to_message:
        await m.reply_text("Usage: .hiraid count username or reply to user")
        return

    # If it's a reply to a message
    if m.reply_to_message:
        try:
            counts = int(m.command[1])
            user = await client.get_users(m.reply_to_message.from_user.id)
        except Exception:
            user = m.reply_to_message.from_user
    else:
        # If user provided count and username
        try:
            counts = int(m.command[1])
            username = m.command[2]
            user = await client.get_users(username)
        except IndexError:
            await m.reply_text("Usage: .hiraid count username")
            return
        except Exception:
            await m.reply_text("**Error:** User not found or maybe deleted!")
            return

    # Anti-spam and protection checks
    if int(m.chat.id) in GROUP:
        await m.reply_text("**Sorry! I can't spam in this group.**")
        return

    if int(user.id) in VERIFIED_USERS:
        await m.reply_text("I can't hiraid my developer.")
        return

    if int(user.id) in SUDO_USER:
        await m.reply_text("This guy is a sudo user.")
        return

    # Perform the raid
    mention = user.mention
    for _ in range(counts):
        r = f"{mention} {choice(HIRAID)}"
        await client.send_message(m.chat.id, r)
        await asyncio.sleep(0.3)
