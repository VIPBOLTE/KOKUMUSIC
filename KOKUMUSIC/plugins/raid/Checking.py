import asyncio
from pyrogram import Client, filters
from config import *

OWNER_ID = 5595153270

clients = []
ACTIVE_SESSIONS = [1, 2, 3]  # Active assistant session numbers


def register_spam_handler(listener_client: Client):
    @listener_client.on_message(filters.command("spam", prefixes=".") & filters.user(OWNER_ID))
    async def spam_handler(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: .spam <count> <message>")

        try:
            count = int(message.command[1])
            text = " ".join(message.command[2:])
        except ValueError:
            return await message.reply("❌ Invalid count! Please use a number.")

        inactive_clients = [clients[i] for i in range(len(clients)) if (i + 1) not in ACTIVE_SESSIONS]

        if not inactive_clients:
            return await message.reply("❌ No inactive clients available!")

        for i in range(count):
            sender_client = inactive_clients[i % len(inactive_clients)]
            try:
                await sender_client.send_message(chat_id=message.chat.id, text=text)
                await asyncio.sleep(1)
            except Exception as e:
                await message.reply(f"⚠️ Failed to send message: {e}")


    global clients
    clients = [
        Client("GOKUAss1", api_id=API_ID, api_hash=API_HASH, session_string=STRING1),
        Client("GOKUAss2", api_id=API_ID, api_hash=API_HASH, session_string=STRING2),
        Client("GOKUAss3", api_id=API_ID, api_hash=API_HASH, session_string=STRING3),
        Client("GOKUAss4", api_id=API_ID, api_hash=API_HASH, session_string=STRING4),
        Client("GOKUAss5", api_id=API_ID, api_hash=API_HASH, session_string=STRING5),
    ]

    for client in clients:
        await client.start()

    register_spam_handler(clients[0])
    print("All clients started and handler registered.")

    await clients[0].idle()  # Keeps the bot running

