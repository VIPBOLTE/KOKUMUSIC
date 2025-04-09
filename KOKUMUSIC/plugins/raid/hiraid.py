import asyncio
from random import choice
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from KOKUMUSIC.misc import SUDOERS as SUDO_USER
from KOKUMUSIC.cplugin.utils.data import (
    HIRAID,
    GROUP,
    VERIFIED_USERS
)

@Client.on_message(filters.command("hiraid", prefixes=".") & SUDO_USER)
async def raid(Client: Client, m: Message):
    args = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)

    if len(args) == 2:
        try:
            counts = int(args[0])
        except ValueError:
            await m.reply_text("Count must be a number.")
            return

        if counts > 100:
            await m.reply_text("Too many messages! Max limit is 100.")
            return

        try:
            user = await Client.get_users(args[1])
        except:
            await m.reply_text("**Error:** User not found or may be deleted!")
            return

    elif m.reply_to_message:
        try:
            counts = int(args[0])
        except (IndexError, ValueError):
            await m.reply_text("Count must be provided and should be a number.")
            return

        try:
            user = await Client.get_users(m.reply_to_message.from_user.id)
        except:
            user = m.reply_to_message.from_user

    else:
        await m.reply_text("Usage: `.hiraid count username` or reply to a user with `.hiraid count`")
        return

    if int(m.chat.id) in GROUP:
        await m.reply_text("**Sorry !! I can't spam here.**")
        return

    if int(user.id) in VERIFIED_USERS:
        await m.reply_text("I can't hiraid on my developer.")
        return

    if int(user.id) in SUDO_USER:
        await m.reply_text("This guy is a sudo user.")
        return

    mention = user.mention
    for _ in range(counts):
        r = f"{mention} {choice(HIRAID)}"
        try:
            await Client.send_message(m.chat.id, r)
            await asyncio.sleep(0.3)
        except FloodWait as e:
            await asyncio.sleep(e.value)
