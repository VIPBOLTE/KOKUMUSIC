import json
import os
import config
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from KOKUMUSIC.core.bot import KOKUBOT
from KOKUMUSIC.core.dir import dirr
from KOKUMUSIC.core.git import git
from KOKUMUSIC.core.userbot import Userbot
from KOKUMUSIC.misc import dbb, heroku, sudo
from .logging import LOGGER
#time zone
TIME_ZONE = pytz.timezone(config.TIME_ZONE)
scheduler = AsyncIOScheduler(timezone=TIME_ZONE)
dirr()
git()
dbb()
heroku()
sudo()
app = KOKUBOT()
userbot = Userbot()
from .platforms import PlaTForms
Platform = PlaTForms()
HELPABLE = {}
