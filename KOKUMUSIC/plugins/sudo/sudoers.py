from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.types import Message
from Strings import get_string, helpers
from KOKUMUSIC import app, SPECIAL_ID
from pyrogram.types import InputMediaVideo
from KOKUMUSIC.music import SUDOERS
from KOKUMUSIC.utils.database import add_sudo, remove_sudo
from KOKUMUSIC.utils.decorators.language import language
from KOKUMUSIC.utils.extraction import extract_user
from KOKUMUSIC.utils.inline import close_markup
from config import BANNED_USERS, OWNER_ID



@app.on_message(filters.command(["addsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID) |filters.user(SPECIAL_ID)) 
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(_["sudo_1"].format(user.mention))
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(_["sudo_2"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])


@app.on_message(filters.command(["delsudo", "rmsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID) |filters.user(SPECIAL_ID))
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    user = await extract_user(message)
    if user.id not in SUDOERS:
        return await message.reply_text(_["sudo_3"].format(user.mention))
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(_["sudo_4"].format(user.mention))
    else:
        await message.reply_text(_["sudo_8"])



@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & ~BANNED_USERS)
async def sudoers_list(client, message: Message):
    keyboard = [[InlineKeyboardButton("๏ ᴠɪᴇᴡ sᴜᴅᴏʟɪsᴛ ๏", callback_data="check_sudo_list")]]
    reply_markups = InlineKeyboardMarkup(keyboard)
  
    #await message.reply_photo(photo="https://telegra.ph/file/a088303b636ff3c2d474a.mp4", caption="**» ᴄʜᴇᴄᴋ sᴜᴅᴏ ʟɪsᴛ ʙʏ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ.**\n\n**» ɴᴏᴛᴇ:**  ᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴠɪᴇᴡ. ", reply_markup=reply_markups)
    await message.reply_video(video="https://envs.sh/K-d.mp4", caption="**» ᴄʜᴇᴄᴋ sᴜᴅᴏ ʟɪsᴛ ʙʏ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ.**\n\n**» ɴᴏᴛᴇ:**  ᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴠɪᴇᴡ. ", reply_markup=reply_markups)
    

@app.on_callback_query(filters.regex("^check_sudo_list$"))
async def check_sudo_list(client, callback_query: CallbackQuery):
    keyboard = []
    if callback_query.from_user.id not in SUDOERS:
        return await callback_query.answer("𝐏𝐞𝐡𝐥𝐢 𝐅𝐮𝐫𝐬𝐚𝐭 𝐌𝐞 𝐍𝐢𝐤𝐚𝐥 𝐁𝐚𝐝𝐚 𝐒𝐮𝐝𝐨𝐥𝐢𝐬𝐭 𝐃𝐞𝐤𝐡𝐧𝐞 𝐀𝐚𝐲𝐚 𝐇𝐚𝐢 𝐛𝐚𝐝𝐚👿😎😂", show_alert=True)
    else:
        user = await app.get_users(OWNER_ID)

        user_mention = (user.first_name if not user.mention else user.mention)
        caption = f"**˹ʟɪsᴛ ᴏғ ʙᴏᴛ ᴍᴏᴅᴇʀᴀᴛᴏʀs˼**\n\n**🌹Oᴡɴᴇʀ** ➥ {user_mention}\n\n"

        keyboard.append([InlineKeyboardButton("๏ ᴠɪᴇᴡ ᴏᴡɴᴇʀ ๏", url=f"tg://openmessage?user_id={OWNER_ID}")])
        
        count = 1
        for user_id in SUDOERS:
            if user_id != OWNER_ID:
                try:
                    user = await app.get_users(user_id)
                    user_mention = user.mention if user else f"**🎁 Sᴜᴅᴏ {count} ɪᴅ:** {user_id}"
                    caption += f"**🎁 Sᴜᴅᴏ** {count} **»** {user_mention}\n"
                    button_text = f"๏ ᴠɪᴇᴡ sᴜᴅᴏ {count} ๏ "
                    keyboard.append([InlineKeyboardButton(button_text, url=f"tg://openmessage?user_id={user_id}")]
                    )
                    count += 1
                except:
                    continue

        # Add a "Back" button at the end
        keyboard.append([InlineKeyboardButton("๏ ʙᴀᴄᴋ ๏", callback_data="back_to_main_menu")])

        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await callback_query.message.edit_caption(caption=caption, reply_markup=reply_markup)

@app.on_callback_query(filters.regex("^back_to_main_menu$"))
async def back_to_main_menu(client, callback_query: CallbackQuery):
    keyboard = [[InlineKeyboardButton("๏ ᴠɪᴇᴡ sᴜᴅᴏʟɪsᴛ ๏", callback_data="check_sudo_list")]]
    reply_markupes = InlineKeyboardMarkup(keyboard)
    await callback_query.message.edit_caption(caption="**» ᴄʜᴇᴄᴋ sᴜᴅᴏ ʟɪsᴛ ʙʏ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ.**\n\n**» ɴᴏᴛᴇ:**  ᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴠɪᴇᴡ. ", reply_markup=reply_markupes)
@app.on_message(filters.command(["delallsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def del_all_sudo(client, message: Message, _):
    removed_users = []  # List to store removed users' information
    for user_id in SUDOERS.copy():
        if user_id != OWNER_ID and user_id != SPECIAL_ID:
            removed = await remove_sudo(user_id)
            if removed:
                SUDOERS.remove(user_id)
                try:
                    user = await app.get_users(user_id)
                    user_mention = user.mention if user else f"ᴜsᴇʀ ɪᴅ: `{user_id}`"
                    removed_users.append(f"{user_mention} `{user_id}`")
                except Exception as e:
                    logging.error(f"ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ᴜsᴇʀ {user_id}: {e}")
                    removed_users.append(f"ᴜsᴇʀ ɪᴅ: `{user_id}`")

    if removed_users:
        removed_users_text = "\n".join(removed_users)
        await message.reply_text(f"ʀᴇᴍᴏᴠᴇᴅ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴜsᴇʀs ғʀᴏᴍ ᴛʜᴇ sᴜᴅᴏ ʟɪsᴛ:\n\n{removed_users_text}")
    else:
        await message.reply_text("ɴᴏ ᴜsᴇʀs ᴡᴇʀᴇ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴛʜᴇ sᴜᴅᴏ ʟɪsᴛ.")
