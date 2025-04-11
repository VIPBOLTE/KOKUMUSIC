import asyncio
from random import choice
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from KOKUMUSIC.misc import SUDOERS as SUDO_USER
from KOKUMUSIC.cplugin.utils.data import HIRAID, VERIFIED_USERS, GROUP

@Client.on_message(filters.command("hiraid", prefixes=".") & SUDO_USER)
async def raid(Client: Client, m: Message):  
    args = m.text.split(maxsplit=2)

    # No args and no reply = show usage
    if len(args) < 2 and not m.reply_to_message:
        return await m.reply_text("Usage: `.hiraid count @username` or reply to a user with `.hiraid count`")

    # Parse count
    try:
        counts = int(args[1])
    except:
        return await m.reply_text("Please provide a valid count. Example: `.hiraid 10 @username`")

    # Fetch user
    user = None
    if len(args) == 3:
        try:
            user = await Client.get_users(args[2])
        except:
            return await m.reply_text("**Error:** Couldn't find the user.")
    elif m.reply_to_message:
        try:
            user = await Client.get_users(m.reply_to_message.from_user.id)
        except:
            user = m.reply_to_message.from_user

    if not user:
        return await m.reply_text("Could not identify the user to raid.")

    # Protection checks
    if m.chat.id in GROUP:
        return await m.reply_text("**Sorry! I can't spam in this group.**")
    
    if user.id in VERIFIED_USERS:
        return await m.reply_text("This user is my developer, I can't hiraid them.")

    if user.id in SUDO_USER:
        return await m.reply_text("Sorry, I can't hiraid this user because they are a SUDO user.")

    # Start raid
    mention = user.mention
    for _ in range(counts): 
        if m.chat.id in GROUP:
            break
        msg = f"{mention} {choice(HIRAID)}"
        try:
            await Client.send_message(m.chat.id, msg)
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        await asyncio.sleep(0.3)
