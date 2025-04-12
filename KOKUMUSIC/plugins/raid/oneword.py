import asyncio
from random import choice
from pyrogram import filters, Client
from pyrogram.types import Message

from KOKUMUSIC.misc import SUDOERS as SUDO_USER
from KOKUMUSIC.cplugin.utils.data import OneWord, GROUP, VERIFIED_USERS


@Client.on_message(filters.command("oneword", prefixes=".") & SUDO_USER)
async def oneword(Client: Client, m: Message):
    Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)

    if len(Bad) == 2:
        try:
            counts = int(Bad[0])
            user = await Client.get_users(Bad[1])
        except Exception:
            await m.reply_text("User not found or invalid input.")
            return
    elif m.reply_to_message:
        try:
            counts = int(Bad[0])
            user = m.reply_to_message.from_user
        except Exception:
            await m.reply_text("Please provide count when replying to message.")
            return
    else:
        await m.reply_text("Usage: .oneword count username or reply")
        return

    if int(m.chat.id) in GROUP:
        await m.reply_text("**Sorry !! I can't spam here.**")
        return
    if int(user.id) in VERIFIED_USERS:
        await m.reply_text("I can't oneword on my developer.")
        return
    if int(user.id) in SUDO_USER:
        await m.reply_text("This guy is a sudo user.")
        return

    mention = user.mention
    for _ in range(counts):
        for word in OneWord:
            await Client.send_message(m.chat.id, f"{mention} {word}")
            await asyncio.sleep(0.2)  # slow it down to avoid floodwait
