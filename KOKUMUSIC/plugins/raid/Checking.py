from pyrogram import Client, filters
from pyrogram.types import Message

# List of allowed admin user IDs
ADMIN_IDS = [5595153270, 7717913705]

@Client.on_message(filters.command("spam") & filters.group)
async def spam_command(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if user is an allowed admin
    if user_id not in ADMIN_IDS:
        return await message.reply_text("⛔ This command is for admins only.")

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        return await message.reply_text("Usage: /spam <count> <message>", quote=True)

    try:
        count = int(args[1])
        if count > 1000:
            return await message.reply_text("⚠️ Max spam limit is 1000.")
    except ValueError:
        return await message.reply_text("❌ Invalid count. Use a number.")

    spam_message = args[2]
    reply_to = message.reply_to_message

    mention = ""
    if reply_to:
        user = reply_to.from_user
        if user:
            mention = f"[{user.first_name}](tg://user?id={user.id}) "
            spam_message = mention + spam_message

    for _ in range(count):
        try:
            await message.reply_text(spam_message, disable_web_page_preview=True)
        except:
            break  # Avoid flood wait crash

    await message.reply_text(f"✅ Spam completed. Sent {count} messages.", quote=True)
