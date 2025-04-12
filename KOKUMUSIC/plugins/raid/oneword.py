import asyncio
from random import choice
from pyrogram import filters, Client
from pyrogram.types import Message

from KOKUMUSIC.misc import SUDOERS as SUDO_USER
from KOKUMUSIC.cplugin.utils.data import OneWord, GROUP, VERIFIED_USERS


@Client.on_message(filters.command("oneword", prefixes=".") & SUDO_USER)
async def oneword(Client: Client, m: Message):  
    args = m.text.split()
    
    if len(args) < 2 and not m.reply_to_message:
        return await m.reply_text("Usage: .oneword count username or reply to a user.")
    
    try:
        count = int(args[1])
    except:
        return await m.reply_text("Invalid count. Please provide a number.")

    if m.reply_to_message:
        user = m.reply_to_message.from_user
    elif len(args) >= 3:
        try:
            user = await Client.get_users(args[2])
        except:
            return await m.reply_text("User not found or invalid username.")
    else:
        return await m.reply_text("Please reply to a user or provide a username.")

    if int(m.chat.id) in GROUP:
        return await m.reply_text("**Sorry! I can't spam in this group.**")
    
    if user.id in VERIFIED_USERS:
        return await m.reply_text("I can't oneword on my developer.")
    
    if user.id in SUDO_USER:
        return await m.reply_text("Sorry, I can't raid this user because they are a sudo user.")

    mention = user.mention
    for _ in range(count):
        msg = f"{mention} {choice(OneWord)}"
        await Client.send_message(m.chat.id, msg)
        await asyncio.sleep(0.3)
