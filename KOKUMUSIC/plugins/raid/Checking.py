import asyncio
import random
import time
from pyrogram.types import Message
from random import choice
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from pyrogram import filters, Client

# import 
from KOKUMUSIC.misc import SUDOERS as SUDO_USER
from KOKUMUSIC.cplugin.utils.data import RAID, PBIRAID, OneWord, HIRAID, PORM, EMOJI, GROUP, VERIFIED_USERS

RUNNING_AAID = set()

@Client.on_message(filters.command("AAID", prefixes=".") & SUDO_USER)
async def emoji(x: Client, e: Message):
    chat_id = e.chat.id

    if chat_id in RUNNING_AAID:
        return await e.reply_text("AAID already running in this chat. Use /stopaaid to stop.")

    RUNNING_AAID.add(chat_id)

    try:
        args = e.text.split(maxsplit=2)
        if len(args) < 2:
            return await e.reply_text(".AAID 10 <ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ ᴏʀ ᴜꜱᴇʀɴᴀᴍᴇ>")

        count = int(args[1])
        target = args[2] if len(args) > 2 else None

        if target:
            ok = await x.get_users(target)
        elif e.reply_to_message:
            ok = await x.get_users(e.reply_to_message.from_user.id)
        else:
            return await e.reply_text(".AAID 10 <ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ ᴏʀ ᴜꜱᴇʀɴᴀᴍᴇ>")

        for _ in range(count):
            if chat_id not in RUNNING_AAID:
                break
            reply = choice(RAID)
            msg = f"[{ok.first_name}](tg://user?id={ok.id}) {reply}"
            await x.send_message(chat_id, msg)
            await asyncio.sleep(0.1)

    except Exception as err:
        await e.reply_text(f"Error: {err}")
    finally:
        RUNNING_AAID.discard(chat_id)



@Client.on_message(filters.command("stopaaid") & SUDO_USER)
async def stop_aaid(_, message: Message):
    chat_id = message.chat.id
    if chat_id in RUNNING_AAID:
        RUNNING_AAID.discard(chat_id)
        await message.reply_text("AAID spam stopped.")
    else:
        await message.reply_text("No AAID spam is running in this chat.")
