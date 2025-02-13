import asyncio
from datetime import datetime
from pyrogram.enums import ChatType
import config
from KOKUMUSIC import app
from KOKUMUSIC.core.call import KOKU, autoend
from KOKUMUSIC.utils.database import get_client, is_active_chat, is_autoend

# Improved auto leave function
async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        while True:
            await asyncio.sleep(config.AUTO_LEAVE_ASSISTANT_TIME)
            from KOKUMUSIC.core.userbot import assistants
            left = 0
            for num in assistants:
                client = await get_client(num)
                try:
                    async for dialog in client.get_dialogs():
                        chat_type = dialog.chat.type
                        # Only check for valid chat types (supergroup, group, channel)
                        if chat_type in [ChatType.SUPERGROUP, ChatType.GROUP, ChatType.CHANNEL]:
                            chat_id = dialog.chat.id
                            # Skip the specified groups
                            if chat_id in [config.LOG_GROUP_ID, -1002159045835, -1002146211959]:
                                continue
                            # Avoid leaving too many chats in one go
                            if left >= 20:
                                break
                            # Leave inactive chat
                            if not await is_active_chat(chat_id):
                                try:
                                    await client.leave_chat(chat_id)
                                    left += 1
                                except Exception as e:
                                    print(f"Error while leaving chat {chat_id}: {e}")
                except Exception as e:
                    print(f"Error while processing dialogs for client {num}: {e}")

# Improved auto end function
async def auto_end():
    while True:
        await asyncio.sleep(5)
        if not await is_autoend():
            continue
        for chat_id, timer in list(autoend.items()):
            if not timer:
                continue
            # Check if the timer has expired
            if datetime.now() > timer:
                # If chat is inactive, remove from autoend
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    continue
                autoend[chat_id] = {}
                try:
                    await KOKU.stop_stream(chat_id)
                except Exception as e:
                    print(f"Error stopping stream for chat {chat_id}: {e}")
                try:
                    await app.send_message(
                        chat_id,
                        "Bᴏᴛ ʜᴀs ʟᴇғᴛ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴅᴜᴇ ᴛᴏ ɪɴᴀᴄᴛɪᴠɪᴛʏ ᴛᴏ ᴀᴠᴏɪᴅ ᴏᴠᴇʀʟᴏᴀᴅ ᴏɴ sᴇʀᴠᴇʀs. Nᴏ-ᴏɴᴇ ᴡᴀs ʟɪsᴛᴇɴɪɴɢ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.",
                    )
                except Exception as e:
                    print(f"Error sending message to chat {chat_id}: {e}")

# Create tasks for auto leave and auto end functions
async def main():
    # Use asyncio.gather to run both tasks concurrently
    await asyncio.gather(
        auto_leave(),
        auto_end()
    )
