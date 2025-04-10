import asyncio
import random
from random import choice
from pyrogram import filters, Client
from pyrogram.types import Message

# Imports from your project
from KOKUMUSIC.misc import SUDOERS as SUDO_USER
from KOKUMUSIC.cplugin.utils.data import RAID, PBIRAID, OneWord, HIRAID, GROUP, VERIFIED_USERS


# PBIRAID
@Client.on_message(filters.command("pbiraid", prefixes=".") & SUDO_USER)
async def pbiraid(Client: Client, m: Message):
    Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
    if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        try:
            user = await Client.get_users(username)
        except:
            await m.reply_text("**Error:** User not found or may be deleted!")
            return
    elif m.reply_to_message:
        counts = int(Bad[0])
        user = m.reply_to_message.from_user
    else:
        await m.reply_text("Usage: .pbiraid count username or reply")
        return

    if int(m.chat.id) in GROUP:
        await m.reply_text("**Sorry !! I can't spam here.**")
        return
    if int(user.id) in VERIFIED_USERS:
        await m.reply_text("I can't pbiraid on my developer.")
        return
    if int(user.id) in SUDO_USER:
        await m.reply_text("This guy is a sudo user.")
        return

    mention = user.mention
    for _ in range(counts):
        r = f"{mention} {choice(PBIRAID)}"
        await Client.send_message(m.chat.id, r)
        await asyncio.sleep(0.3)


# ONEWORDAID
@Client.on_message(filters.command("oneword", prefixes=".") & SUDO_USER)
async def oneword(Client: Client, m: Message):
    Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
    if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        try:
            user = await Client.get_users(username)
        except:
            await m.reply_text("**Error:** User not found or may be deleted!")
            return
    elif m.reply_to_message:
        counts = int(Bad[0])
        user = m.reply_to_message.from_user
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
        r = f"{mention} {choice(OneWord)}"
        await Client.send_message(m.chat.id, r)
        await asyncio.sleep(0.3)


# HIRAID
@Client.on_message(filters.command("hiraid", prefixes=".") & SUDO_USER)
async def hiraid(Client: Client, m: Message):
    Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
    if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        try:
            user = await Client.get_users(username)
        except:
            await m.reply_text("**Error:** User not found or may be deleted!")
            return
    elif m.reply_to_message:
        counts = int(Bad[0])
        user = m.reply_to_message.from_user
    else:
        await m.reply_text("Usage: .hiraid count username or reply")
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
        await Client.send_message(m.chat.id, r)
        await asyncio.sleep(0.3)


# RAID
@Client.on_message(filters.command("raid", prefixes=".") & SUDO_USER)
async def raid(Client: Client, m: Message):
    Bad = "".join(m.text.split(maxsplit=1)[1:]).split(" ", 2)
    if len(Bad) == 2:
        counts = int(Bad[0])
        username = Bad[1]
        try:
            user = await Client.get_users(username)
        except:
            await m.reply_text("**Error:** User not found or may be deleted!")
            return
    elif m.reply_to_message:
        counts = int(Bad[0])
        user = m.reply_to_message.from_user
    else:
        await m.reply_text("Usage: .raid count username or reply")
        return

    if int(m.chat.id) in GROUP:
        await m.reply_text("**Sorry !! I can't spam here.**")
        return
    if int(user.id) in VERIFIED_USERS:
        await m.reply_text("I can't raid on my developer.")
        return
    if int(user.id) in SUDO_USER:
        await m.reply_text("This guy is a sudo user.")
        return

    mention = user.mention
    for _ in range(counts):
        r = f"{mention} {choice(RAID)}"
        await Client.send_message(m.chat.id, r)
        await asyncio.sleep(0.3)
