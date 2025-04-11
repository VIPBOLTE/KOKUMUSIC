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

@Client.on_message(filters.command("emojii", prefixes=".") & SUDO_USER)
async def emoji(x: Client, e: Message):
      PBX = "".join(e.text.split(maxsplit=1)[1:]).split(" ", 2)

      if len(PBX) == 2:
          ok = await x.get_users(PBX[1])
          counts = int(PBX[0])
          for _ in range(counts):
                reply = choice(EMOJI)
                msg = f"[{ok.first_name}](tg://user?id={ok.id}) {reply}"
                await x.send_message(e.chat.id, msg)
                await asyncio.sleep(0.1)

      elif e.reply_to_message:
          user_id = e.reply_to_message.from_user.id
          ok = await x.get_users(user_id)
          counts = int(PBX[0])
          for _ in range(counts):
                reply = choice(EMOJI)
                msg = f"[{ok.first_name}](tg://user?id={ok.id}) {reply}"
                await x.send_message(e.chat.id, msg)
                await asyncio.sleep(0.1)

      else:
            await e.reply_text(".emojii 10 <ʀᴇᴘʟʏ ᴛᴏ ᴜꜱᴇʀ ᴏʀ ᴜꜱᴇʀɴᴀᴍᴇ>")
            

              
