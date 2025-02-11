import asyncio
import importlib

from pyrogram import idle

import config
from config import BANNED_USERS
from KOKUMUSIC import HELPABLE, LOGGER, app, userbot
from KOKUMUSIC.core.call import KOKU  # Ensure KOKU is initialized correctly
from KOKUMUSIC.plugins import ALL_MODULES
from KOKUMUSIC.utils.database import get_banned_users, get_gbanned


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("KOKUMUSIC").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("KOKUMUSIC").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass

    # Start Pyrogram client
    await app.start()
    LOGGER("KOKUMUSIC").info("Pyrogram client started!")

    # Import all modules
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    LOGGER("KOKUMUSIC.plugins").info("Successfully Imported All Modules ")

    # Start userbot
    await userbot.start()
    LOGGER("KOKUMUSIC").info("Userbot started!")

    # Start pytgcalls
    await KOKU.start()
    LOGGER("KOKUMUSIC").info("PyTgCalls started!")

    # Run decorators (if any)
    await KOKU.decorators()
    LOGGER("KOKUMUSIC").info("KOKUMUSIC STARTED SUCCESSFULLY 🕊️")

    # Idle
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop_policy().get_event_loop().run_until_complete(init())
    LOGGER("KOKUMUSIC").info("Stopping KOKUMUSIC! GoodBye")
