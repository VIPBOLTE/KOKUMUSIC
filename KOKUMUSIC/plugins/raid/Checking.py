from pyrogram import Client, filters
import asyncio

OWNER_ID = 5595153270  # Your OWNER_ID
clients = []  # Fill this list with active Pyrogram clients
ACTIVE_SESSIONS = [1, 2, 3]  # Active assistant session numbers

async def initialize_clients():
    """Ensure all clients are initialized properly."""
    global clients
    clients = [
        Client("GOKUAss1", api_id=API_ID, api_hash=API_HASH, session_string=),
        Client("GOKUAss2", api_id=API_ID, api_hash=API_HASH, session_string="session_2"),
        Client("GOKUAss3", api_id=API_ID, api_hash=API_HASH, session_string="session_3"),
        Client("GOKUAss4", api_id=API_ID, api_hash=API_HASH, session_string="session_4"),
        Client("GOKUAss5", api_id=API_ID, api_hash=API_HASH, session_string="session_5"),
    ]

    # Start all clients
    for client in clients:
        await client.start()

@clients[0].on_message(filters.command("spam", prefixes=".") & filters.user(OWNER_ID))
async def spam_handler(client, message):
    if len(message.command) < 3:
        return await message.reply("Usage: .spam <count> <message>")

    try:
        count = int(message.command[1])
        text = " ".join(message.command[2:])
    except ValueError:
        return await message.reply("❌ Invalid count! Please use a number.")

    inactive_clients = [clients[i - 1] for i in range(len(clients)) if (i + 1) not in ACTIVE_SESSIONS]

    if not inactive_clients:
        return await message.reply("❌ No inactive clients available!")

    for i in range(count):
        client = inactive_clients[i % len(inactive_clients)]
        try:
            await client.send_message(chat_id=message.chat.id, text=text)
            await asyncio.sleep(1)  # 1-second delay to avoid flood wait
        except Exception as e:
            await message.reply(f"⚠️ Failed to send message: {e}")

# Run the initialization before using clients
asyncio.run(initialize_clients())
